import Cocoa
import ApplicationServices

let args = CommandLine.arguments
func attr(_ e: AXUIElement, _ key: String) -> CFTypeRef? {
    var v: CFTypeRef?; return AXUIElementCopyAttributeValue(e, key as CFString, &v) == .success ? v : nil
}
func str(_ e: AXUIElement, _ key: String) -> String { (attr(e,key) as? String) ?? "" }
func walk(_ e: AXUIElement, _ depth: Int, _ maxDepth: Int, _ lines: inout [String]) {
    if lines.count > 1800 { return }
    let role = str(e,"AXRole"), title = str(e,"AXTitle"), desc = str(e,"AXDescription")
    let value = str(e,"AXValue")
    var pos = CGPoint.zero, size = CGSize.zero
    if let v = attr(e,"AXPosition"), CFGetTypeID(v) == AXValueGetTypeID() { AXValueGetValue(v as! AXValue, .cgPoint, &pos) }
    if let v = attr(e,"AXSize"), CFGetTypeID(v) == AXValueGetTypeID() { AXValueGetValue(v as! AXValue, .cgSize, &size) }
    lines.append(String(repeating:" ",count:depth) + "\(role) | \(title) | \(desc) | \(value.prefix(200)) | \(Int(pos.x)),\(Int(pos.y)),\(Int(size.width)),\(Int(size.height))")
    if depth < maxDepth, let children = attr(e,"AXChildren") as? [AXUIElement] { for child in children { walk(child,depth+1,maxDepth,&lines) } }
}
func app(_ id: String) -> NSRunningApplication? { NSWorkspace.shared.runningApplications.first { $0.bundleIdentifier == id } }
if args.count < 2 { exit(1) }
switch args[1] {
case "apps":
    print("AXTrusted=\(AXIsProcessTrusted())")
    for a in NSWorkspace.shared.runningApplications where a.activationPolicy == .regular { print("\(a.processIdentifier) | \(a.bundleIdentifier ?? "") | \(a.localizedName ?? "")") }
case "activate":
    guard let a = app(args[2]) else { print("App not running"); exit(2) }; a.activate(options:[.activateIgnoringOtherApps]); Thread.sleep(forTimeInterval:0.5)
case "ax":
    guard let a = app(args[2]) else { exit(2) }; var lines:[String]=[]; walk(AXUIElementCreateApplication(a.processIdentifier),0,Int(args.count>3 ? args[3]:"8") ?? 8,&lines); print(lines.joined(separator:"\n"))
case "click":
    let p=CGPoint(x:Double(args[2])!,y:Double(args[3])!)
    CGEvent(mouseEventSource:nil,mouseType:.mouseMoved,mouseCursorPosition:p,mouseButton:.left)?.post(tap:.cghidEventTap)
    for type:CGEventType in [.leftMouseDown,.leftMouseUp] { CGEvent(mouseEventSource:nil,mouseType:type,mouseCursorPosition:p,mouseButton:.left)?.post(tap:.cghidEventTap) }
case "key":
    let code=CGKeyCode(args[2])!; var flags:CGEventFlags=[]
    if args.count>3 { if args[3].contains("cmd") {flags.insert(.maskCommand)}; if args[3].contains("shift") {flags.insert(.maskShift)}; if args[3].contains("alt") {flags.insert(.maskAlternate)}; if args[3].contains("ctrl") {flags.insert(.maskControl)} }
    for down in [true,false] { let e=CGEvent(keyboardEventSource:nil,virtualKey:code,keyDown:down); e?.flags=flags; e?.post(tap:.cghidEventTap) }
case "paste":
    let s=try String(contentsOfFile:args[2],encoding:.utf8); let pb=NSPasteboard.general; pb.clearContents(); pb.setString(s,forType:.string)
    for down in [true,false] { let e=CGEvent(keyboardEventSource:nil,virtualKey:9,keyDown:down); e?.flags = .maskCommand; e?.post(tap:.cghidEventTap) }
case "screen":
    let p=Process(); p.executableURL=URL(fileURLWithPath:"/usr/sbin/screencapture");p.arguments=["-x",args[2]];try p.run();p.waitUntilExit();exit(p.terminationStatus)
default: exit(1)
}
