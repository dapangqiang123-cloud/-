function run(args) {
  var se = Application('System Events');
  function proc(id){for(var j=0;j<se.applicationProcesses.length;j++){var p=se.applicationProcesses[j];if(p.bundleIdentifier()===id)return se.applicationProcesses[j];}throw new Error('Process not found: '+id); }
  function win(p,term){for(var k=0;k<p.windows.length;k++){if(p.windows[k].name().indexOf(term)>=0)return p.windows[k];}throw new Error('Window not found: '+term); }
  if(args[0]==='pathaction'){var p=proc(args[1]),e=win(p,args[2]);JSON.parse(args[3]).forEach(function(n){e=e.uiElements[n];});if(args[4]==='value')e.value=args[5];else if(args[4]==='click')e.click();else e.actions.byName(args[4]||'AXPress').perform();return JSON.stringify(e.properties());}
  if(args[0]==='tree'||args[0]==='treepress'||args[0]==='treeedit'){var p=proc(args[1]),w=win(p,args[2]),out=[],count=0,done=false; function walk(e,path,depth){if(done||count++>1500||depth>25)return;var o;try{o=e.properties();}catch(ex){return;}if(args[0]==='treeedit'&&o.role==='AXTextArea'){e.attributes.byName('AXFocused').value=true;e.click();run(['key','0','command down',args[1]]);run(['paste',args[3],'',args[1]]);out=[{path:path,value:e.value()}];done=true;return;}if(args[0]==='treepress'&&(o.name===args[3]||o.description===args[3])){e.actions.byName('AXPress').perform();done=true;return;} if(!['AXGroup','AXScrollArea','AXSplitGroup','AXTabGroup'].includes(o.role))out.push({path:path,role:o.role,name:o.name,description:o.description,value:o.value,position:o.position,size:o.size});var n;try{n=e.uiElements.length;}catch(ex){return;}for(var i=0;i<n;i++){try{walk(e.uiElements[i],path.concat(i),depth+1);}catch(ex){}}} walk(w,[],0);if(args[0]==='treepress'){if(!done)throw new Error('Control not found: '+args[3]);return 'pressed '+args[3];}return JSON.stringify(out); }
  if(args[0]==='appsindex'){var out=[];for(var i=0;i<se.applicationProcesses.length;i++){var p=se.applicationProcesses[i];if(p.name()==='Web App')out.push({index:i,name:p.name(),bundle:p.bundleIdentifier(),pid:p.unixId(),windows:p.windows.name()});}return JSON.stringify(out); }
  if(args[0]==='menu'){var p=proc(args[1]);var m=p.menuBars[0].menuBarItems.byName(args[2]);if(args[3])m.menus[0].menuItems.byName(args[3]).click();return JSON.stringify(m.menus[0].menuItems.name());}
  if(args[0]==='apps')return JSON.stringify(se.applicationProcesses.whose({backgroundOnly:false})().map(function(p){return {name:p.name(),bundle:p.bundleIdentifier(),pid:p.unixId()};}));
  if(args[0]==='release'){se.keyUp('command');se.keyUp('shift');se.keyUp('option');se.keyUp('control');return 'released';}
  if(args[0]==='a11y'){var p=proc(args[1]);var names=p.attributes.name();if(args[2])p.attributes.byName(args[2]).value=true;return JSON.stringify(names); }
  if(args[0]==='layout'){
    var p=proc(args[1]);
    var w=p.windows.whose({name:{_contains:args[2]}})[0];
    w.position=[Number(args[3]),Number(args[4])];w.size=[Number(args[5]),Number(args[6])];
    p.frontmost=true;w.actions.byName('AXRaise').perform();delay(0.5);
    return JSON.stringify({position:w.position(),size:w.size()});
  }
  if(args[0]==='indexaction'){
    var p=proc(args[1]);
    var w=win(p,args[2]),e=w.entireContents()[Number(args[3])],o=e.properties();
    if(o.role!==args[4])throw new Error('Role changed');
    if(args[5]==='info')return JSON.stringify({properties:o,actions:e.actions.name(),attributes:e.attributes.name()});
    if(args[5]==='focus')e.attributes.byName('AXFocused').value=true;else if(args[5]==='value')e.value=args[6];else if(args[5]==='click')e.click();else e.actions.byName(args[5]||'AXPress').perform();
    return JSON.stringify({role:o.role,name:o.name,description:o.description,position:o.position,value:e.value()});
  }
  if(args[0]==='press'||args[0]==='setvalue'){
    var p=proc(args[1]);
    p.frontmost=true;delay(0.1);
    var w=win(p,args[2]);var els=w.entireContents();
    for(var i=0;i<els.length;i++){
      var o;try{o=els[i].properties();}catch(ex){continue;}
      if(o.name===args[3]||o.description===args[3]){
        if(args[0]==='setvalue'){els[i].value=args[4];return 'set '+args[3];}
        els[i].actions.byName('AXPress').perform();return 'pressed '+args[3];
      }
    }throw new Error('Control not found: '+args[3]);
  }
  if(args[0]==='elements'){
    var p=proc(args[1]);
    var w=win(p,args[2]);
    var els=w.entireContents(),out=[];
    for(var i=0;i<els.length&&i<Number(args[3]||2000);i++){
      var e=els[i],o;try{o=e.properties();}catch(ex){continue;}
      if(['AXGroup','AXSplitGroup','AXTabGroup','AXScrollArea'].indexOf(o.role)>=0)continue;
      out.push({index:i,role:o.role,name:o.name,description:o.description,value:typeof o.value==='string'?o.value.slice(0,300):null,position:o.position,size:o.size});
    }
    return JSON.stringify({count:els.length,elements:out});
  }
  if(args[0]==='rightclick'){
    var p=proc(args[3]||'com.apple.Safari.WebApp.892C8620-3812-47C7-8DFE-CE9B0FC2C0BF');p.frontmost=true;delay(0.3);
    ObjC.import('CoreGraphics');var point={x:Number(args[1]),y:Number(args[2])};
    $.CGEventPost(0,$.CGEventCreateMouseEvent(null,3,point,1));delay(0.1);$.CGEventPost(0,$.CGEventCreateMouseEvent(null,4,point,1));return 'right clicked';
  }
  if(args[0]==='fastax'){
    ObjC.import('ApplicationServices');var pid=proc(args[1]).unixId();
    var root=$.AXUIElementCreateApplication(pid),out=[],count=0,maxDepth=Number(args[2]||15);
    function attr(e,k){var r=Ref();var err=$.AXUIElementCopyAttributeValue(e,$(k),r);return err===0?r[0]:null;}
    function value(e,k){var v=attr(e,k);if(!v)return null;try{return ObjC.unwrap(v);}catch(ex){return String(v);}}
    function walk(e,depth,path){if(count++>3000)return;var role=value(e,'AXRole'),title=value(e,'AXTitle'),desc=value(e,'AXDescription'),val=value(e,'AXValue');
      if(title||desc||role==='AXButton'||role==='AXTextArea'||role==='AXTextField')out.push({path:path,role:role,title:title,description:desc,value:typeof val==='string'?val.slice(0,300):null,position:String(attr(e,'AXPosition')),size:String(attr(e,'AXSize'))});
      if(depth<maxDepth){var ch=attr(e,'AXChildren');if(ch){for(var i=0;i<ch.count;i++)walk(ch.objectAtIndex(i),depth+1,path+'/'+i);}}
    }
    walk(root,0,'');return JSON.stringify(out);
  }
  if(args[0]==='cgclick'){
    Application(args[3]||'com.apple.Safari.WebApp.892C8620-3812-47C7-8DFE-CE9B0FC2C0BF').activate();delay(0.3);
    var p=proc(args[3]||'com.apple.Safari.WebApp.892C8620-3812-47C7-8DFE-CE9B0FC2C0BF');
    p.frontmost=true;delay(0.3);
    if(args[4]==='raise'){p.windows[0].actions.byName('AXRaise').perform();delay(0.3);}
    ObjC.import('CoreGraphics');var point={x:Number(args[1]),y:Number(args[2])};
    $.CGEventPost(0,$.CGEventCreateMouseEvent(null,5,point,0));
    $.CGEventPost(0,$.CGEventCreateMouseEvent(null,1,point,0));
    $.CGEventPost(0,$.CGEventCreateMouseEvent(null,2,point,0));
    return JSON.stringify($.CGEventGetLocation($.CGEventCreate(null)));
  }
  if(args[0]==='front') {return JSON.stringify(se.applicationProcesses.whose({frontmost:true}).name());}
  if(args[0]==='screen'){
    var current=Application.currentApplication();current.includeStandardAdditions=true;
    if(!/^\/private\/tmp\/[a-zA-Z0-9_]+\.png$/.test(args[1]))throw new Error('Invalid screenshot path');
    delay(0.4);current.doShellScript('/usr/sbin/screencapture -x -D'+(args[2]==='2'?'2':'1')+' '+args[1]);return 'captured';
  }
  if(args[0]==='batch'){
    ObjC.import('Foundation');var s=ObjC.unwrap($.NSString.stringWithContentsOfFileEncodingError(args[1],$.NSUTF8StringEncoding,null));
    return JSON.stringify(JSON.parse(s).map(function(step){if(step[0]==='wait'){delay(Number(step[1]));return 'waited';}return run(step);}));
  }
  if (args[0] === 'screens') {
    ObjC.import('AppKit');var out=[];var screens=$.NSScreen.screens;
    for(var i=0;i<screens.count;i++){var s=screens.objectAtIndex(i);out.push({frame:s.frame,scale:s.backingScaleFactor,name:ObjC.unwrap(s.localizedName)});}
    return JSON.stringify(out);
  }
  if (args[0] === 'focus') {
    var p=proc(args[1]);
    p.frontmost=true;
    var w=p.windows[Number(args[2]||0)];
    w.actions.byName('AXRaise').perform();
    if(args[3])w.position=[Number(args[3]),Number(args[4])];
    return 'focused';
  }
  if (args[0] === 'activate') { Application(args[1]).activate(); return 'activated'; }
  if (args[0] === 'windows') {
    var p = se.applicationProcesses.whose({bundleIdentifier: args[1]})[0];
    return JSON.stringify(p.windows().map(function(w){return {name:w.name(),position:w.position(),size:w.size()};}));
  }
  if (args[0] === 'click') {
    Application(args[3]||'com.apple.Safari.WebApp.892C8620-3812-47C7-8DFE-CE9B0FC2C0BF').activate();delay(0.3);
    if(args[3]) {
      var p=proc(args[3]);p.frontmost=true;
      p.windows[0].actions.byName('AXRaise').perform();delay(0.4);
    }
    var current=Application.currentApplication();current.includeStandardAdditions=true;
    var hold=args[4]==='command'?'command':args[4]==='shift'?'shift':null;
    var code='tell application "System Events"\n'+(hold?'key down '+hold+'\n':'')+'click at {'+Number(args[1])+','+Number(args[2])+'}\n'+(hold?'key up '+hold+'\n':'')+'end tell';
    current.doShellScript("/usr/bin/osascript -e '"+code+"'");
    return 'clicked';
  }
  if (args[0] === 'key') {
    var current=Application.currentApplication();current.includeStandardAdditions=true;
    var modifier=args[2] ? ' using {'+args[2].split(',').filter(function(x){return ['command down','shift down','option down','control down'].indexOf(x)>=0;}).join(',')+'}' : '';
    Application(args[3]||'com.apple.Safari.WebApp.892C8620-3812-47C7-8DFE-CE9B0FC2C0BF').activate();delay(0.2);
    current.doShellScript("/usr/bin/osascript -e 'tell application \"System Events\" to key code "+Number(args[1])+modifier+"'");return 'key';
  }
  if (args[0] === 'paste') {
    Application(args[3]||'com.apple.Safari.WebApp.892C8620-3812-47C7-8DFE-CE9B0FC2C0BF').activate();delay(0.2);
    ObjC.import('AppKit');ObjC.import('Foundation');
    var s=$.NSString.stringWithContentsOfFileEncodingError(args[1],$.NSUTF8StringEncoding,null);
    var pb=$.NSPasteboard.generalPasteboard;pb.clearContents;pb.setStringForType(s,$.NSPasteboardTypeString);
    var current=Application.currentApplication();current.includeStandardAdditions=true;
    current.doShellScript("/usr/bin/osascript -e 'tell application \"System Events\" to keystroke \"v\" using {command down}'");return 'pasted';
  }
  if (args[0] === 'ax') {
    var p=proc(args[1]);
    var maxDepth=Number(args[2]||8), lines=[];
    function read(e,n) {
      if(lines.length>1800)return;
      var o={depth:n};
      ['role','name','description','value','position','size'].forEach(function(k){try{o[k]=e[k]();}catch(ex){}});
      lines.push(o);
      if(n<maxDepth){var ch=[];try{ch=e.uiElements();}catch(ex){};ch.forEach(function(c){read(c,n+1);});}
    }
    p.windows().filter(function(w){return !args[3]||w.name().indexOf(args[3])>=0;}).forEach(function(w){read(w,0);});return JSON.stringify(lines);
  }
  throw new Error('Unknown action');
}
