#!/usr/bin/env python3
"""Scale an approved edit plan to a VO duration; does not alter media."""
import argparse
import json
import math
import subprocess
from pathlib import Path


def retime(plan, seconds):
    fps = plan["fps"]
    if not math.isfinite(seconds) or seconds <= 0:
        raise ValueError("Duration must be a positive finite number")
    total = math.floor(seconds * fps + 0.5)
    original = plan.get("base_total_frames", plan["total_frames"])
    result = json.loads(json.dumps(plan))
    result["base_total_frames"] = original
    result["total_frames"] = total
    result["duration_seconds"] = total / fps
    result["requested_duration_seconds"] = seconds
    result["retime_scale"] = total / original
    result["status"] = "retimed_plan_requires_render_and_review"

    def boundary(frame):
        return (2 * frame * total + original) // (2 * original)

    for shot in result["shots"]:
        a = shot.setdefault("base_start_frame", shot["start_frame"])
        b = shot.setdefault("base_end_frame", shot["end_frame"])
        shot["start_frame"] = boundary(a)
        shot["end_frame"] = boundary(b)
        shot["duration_frames"] = shot["end_frame"] - shot["start_frame"]
        if shot["duration_frames"] < 1:
            raise ValueError("Requested duration collapses a shot to zero frames")
        for key in ("start", "end", "duration"):
            shot[key + "_seconds"] = shot[key + "_frame" if key != "duration" else "duration_frames"] / fps
        shot["status"] = "planned_not_rendered"
    assert result["shots"][0]["start_frame"] == 0
    assert result["shots"][-1]["end_frame"] == total
    assert all(a["end_frame"] == b["start_frame"] for a, b in zip(result["shots"], result["shots"][1:]))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("timing.json"))
    duration = parser.add_mutually_exclusive_group(required=True)
    duration.add_argument("--duration", type=float)
    duration.add_argument("--voiceover", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    seconds = args.duration
    if args.voiceover:
        probe = subprocess.run(
            ["/opt/homebrew/bin/ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(args.voiceover)],
            check=True, capture_output=True, text=True,
        )
        seconds = float(json.loads(probe.stdout)["format"]["duration"])
    plan = retime(json.loads(args.input.read_text()), seconds)
    if args.output.resolve() == args.input.resolve():
        parser.error("Use a separate output file to preserve the original plan")
    args.output.write_text(json.dumps(plan, ensure_ascii=False, indent=2))
    print(f"{len(plan['shots'])} shots; {plan['total_frames']} frames; {plan['duration_seconds']:.3f}s; {args.output}")


if __name__ == "__main__":
    main()
