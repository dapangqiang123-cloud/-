import Foundation
import Vision
import ImageIO

let dir = URL(fileURLWithPath: CommandLine.arguments[1])
let files = try FileManager.default.contentsOfDirectory(at: dir, includingPropertiesForKeys: nil).filter { $0.pathExtension.lowercased() == "png" }.sorted { $0.lastPathComponent < $1.lastPathComponent }
var result: [[String: Any]] = []
for file in files {
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.recognitionLanguages = ["zh-Hans", "en-US"]
    req.usesLanguageCorrection = false
    req.usesCPUOnly = true
    do { try VNImageRequestHandler(url: file).perform([req]) }
    catch { result.append(["file": file.lastPathComponent, "error": String(describing: error)]); continue }
    let found: [[String: Any]] = (req.results ?? []).compactMap { item in
        guard let text = item.topCandidates(1).first, text.confidence > 0.25 else { return nil }
        return ["text": text.string, "confidence": text.confidence, "box": [item.boundingBox.minX, item.boundingBox.minY, item.boundingBox.width, item.boundingBox.height]]
    }
    result.append(["file": file.lastPathComponent, "text": found])
}
let data = try JSONSerialization.data(withJSONObject: result, options: [.prettyPrinted, .sortedKeys])
print(String(data: data, encoding: .utf8)!)
