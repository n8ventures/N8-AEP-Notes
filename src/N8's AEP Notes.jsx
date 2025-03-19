function notesPanel(thisObj) {
    var win = (thisObj instanceof Panel) ?
        thisObj :
        new Window("palette", "N8's AEP Notes", undefined, {
            resizeable: true
        });

    // Build UI
    win.orientation = "column";
    win.alignChildren = ["fill", "top"];
    win.spacing = 10;
    win.margins = 12;
    win.minimumSize = [300, 400];

    var notesBox = win.add("edittext", undefined, "", {
        multiline: true,
        scrolling: true
    });
    notesBox.preferredSize.height = 300;
    notesBox.minimumSize.height = 150;

    var infoText = win.add("statictext", undefined, "");
    infoText.alignment = ["fill", "center"];
    infoText.justify = "center";

    var buttonGroup = win.add("group");
    buttonGroup.orientation = "row";
    buttonGroup.alignChildren = ["fill", "center"];
    buttonGroup.alignment = "fill";

    var loadBtn = buttonGroup.add("button", undefined, "Load");
    var saveBtn = buttonGroup.add("button", undefined, "Save");
    var clearBtn = buttonGroup.add("button", undefined, "Clear");

    function getProjectFolder() {
        return app.project.file ? app.project.file.parent.fsName : null;
    }

    function updateUIState() {
        var projectFolder = getProjectFolder();
        if (!projectFolder) {
            infoText.text = "Save your project to enable Load/Save.";
            loadBtn.enabled = false;
            saveBtn.enabled = false;
        } else {
            infoText.text = "";
            loadBtn.enabled = true;
            saveBtn.enabled = true;
        }
    }

    function loadNotesFile() {
        var projectFolder = getProjectFolder();
        if (!projectFolder) return;

        var xmlFile = new File(projectFolder + "/project-notes.xml");
        var txtFile = new File(projectFolder + "/project-notes.txt");
        var fileToLoad = null;

        if (xmlFile.exists) fileToLoad = xmlFile;
        else if (txtFile.exists) fileToLoad = txtFile;

        if (fileToLoad && fileToLoad.open("r")) {
            var contents = fileToLoad.read();
            fileToLoad.close();

            if (fileToLoad.name.match(/\.xml$/)) {
                var noteMatch = contents.match(/<notes>([\s\S]*?)<\/notes>/);
                notesBox.text = noteMatch ? noteMatch[1] : contents;
            } else {
                notesBox.text = contents;
            }
        }
    }

    function saveNotesFile() {
        var projectFolder = getProjectFolder();
        if (!projectFolder) {
            alert("Save project first!");
            return;
        }

        var xmlFile = new File(projectFolder + "/project-notes.xml");
        if (xmlFile.open("w")) {
            var xmlContent = "<notes>" + notesBox.text + "</notes>";
            xmlFile.write(xmlContent);
            xmlFile.close();
            alert("Notes saved!");
        }
    }

    loadBtn.onClick = loadNotesFile;
    saveBtn.onClick = saveNotesFile;
    clearBtn.onClick = function() {
        notesBox.text = "";
    };

    win.onShow = function() {
        updateUIState();
        loadNotesFile();
    };

    win.onResizing = win.onResize = function() {
        this.layout.resize();
    };

    win.layout.layout(true);
    return win;
}

// Important! Return the panel for Adobe’s dockable system:
var myScriptPanel = notesPanel(this);
if (myScriptPanel instanceof Window) {
    myScriptPanel.center();
    myScriptPanel.show();
}