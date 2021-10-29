function _isVisible(elem) {
    var el = elem[0];
    return el.offsetWidth > 0 && el.offsetHeight > 0;
}
function Confirm_js() {
    var confirm_value = document.createElement("INPUT");
    confirm_value.type = "hidden";
    confirm_value.name = "confirm_value";
    if (confirm("Do you want to save data?")) {
        confirm_value.value = "Yes";
    } else {
        confirm_value.value = "No";
    }
    document.forms[0].appendChild(confirm_value);
}
function update_filename() {
    var wzdescription = document.getElementById("txt_workzonedescription").value;
    var roadname = document.getElementById("txtRoadName").value;
    //Verify valid chars and length for filename
    var strfilename_wzdescription = wzdescription.toLowerCase();
    var strfilename_roadname = roadname.toLowerCase();

    var filenameRegex = /[^a-zA-Z0-9\-]/g;
    var validName_wzdescription = strfilename_wzdescription.replace(filenameRegex, "-");
    var validName_roadname = strfilename_roadname.replace(filenameRegex, "-");
    document.getElementById("txtFilepath_configSave").enabled = false;
    document.getElementById("txtFilepath_configSave").value = "config--" + validName_wzdescription + "--" + validName_roadname + ".json";
    document.getElementById("btnDownloadFile").disabled = true
    document.getElementById("btnDownloadFile").style.color = "gray";
    document.getElementById("btnPublishFile").disabled = true
    document.getElementById("btnPublishFile").style.color = "gray";
    document.getElementById("btnDownloadFile_tab1").disabled = true
    document.getElementById("btnDownloadFile_tab1").style.color = "gray";
    document.getElementById("txtConfigType").value = "Config status: File name has changed, this configuration data will be saved to a new file.";
    document.getElementById("txtFilepath_configSave").enabled = true;
    //Clear fields and map location
    clear_markers();
}
function MutExChkList(chk) {
    var chkList = chk.parentNode.parentNode.parentNode;
    var chks = chkList.getElementsByTagName("input");
    for (var i = 0; i < chks.length; i++) {
        if (chks[i] != chk && chk.checked) {
            chks[i].checked = false;
        }
    }
}
function check_requiredfields() {
    var valid = false;
    var valid_msg = "";
    var ddnumberoflanes = document.getElementById("dd_numberoflanes");
    var ddnumberoflanes_val = ddnumberoflanes.options[ddnumberoflanes.selectedIndex].value;
    if ((document.getElementById("dd_numberoflanes").value >= 1)) {
        valid = true;
    }
    else {
        valid = false;
        valid_msg = " Number of lanes";
    }
    document.getElementById("txtRequiredFields_Valid").value = valid;
    document.getElementById("txtRequiredFields_Text").Text = valid_msg;
    submitbtn();
}



function validateFloatKeyPress(el, evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode;
    var number = el.value.split('.');
    if (charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    }
    //just one dot
    if (number.length > 1 && charCode == 46) {
        return false;
    }
    //get the carat position
    var caratPos = getSelectionStart(el);
    var dotPos = el.value.indexOf(".");
    if (caratPos > dotPos && dotPos > -1 && (number[1].length > 1)) {
        return false;
    }
    return true;
}
function formatTime(timeInput, evt) {

    intValidNum = timeInput.value;
    var charCode = (evt.which) ? evt.which : event.keyCode;
    if (charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 58)) {

        return false;
    }
    if (intValidNum < 24 && intValidNum.length == 2) {
        timeInput.value = timeInput.value + ":";
        return false;
    }
    if (intValidNum == 24 && intValidNum.length == 2) {
        timeInput.value = timeInput.value.length - 2 + "0:";
        return false;
    }
    if (intValidNum > 24 && intValidNum.length == 2) {
        timeInput.value = "";
        return false;
    }

    if (intValidNum.length == 5 && intValidNum.slice(-2) < 60) {
        timeInput.value = timeInput.value + ":";
        return false;
    }
    if (intValidNum.length == 5 && intValidNum.slice(-2) > 60) {
        timeInput.value = timeInput.value.slice(0, 2) + ":";
        return false;
    }
    if (intValidNum.length == 5 && intValidNum.slice(-2) == 60) {
        timeInput.value = timeInput.value.slice(0, 2) + ":00:";
        return false;
    }


    if (intValidNum.length == 8 && intValidNum.slice(-2) > 60) {
        timeInput.value = timeInput.value.slice(0, 5) + ":";
        return false;
    }
    if (intValidNum.length == 8 && intValidNum.slice(-2) == 60) {
        timeInput.value = timeInput.value.slice(0, 5) + ":00";
        return false;
    }
}
function showContent() {
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "progressBar": true,
        "preventDuplicates": false,
        "positionClass": "toast-bottom-full-width",
        "showDuration": "400",
        "hideDuration": "1000",
        "timeOut": "7000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    }
    var strmsg = document.getElementById("hdnParam").value;
    var errortype = document.getElementById("msgtype").value;

    if (errortype == "Success") {
        toastr["success"](strmsg, "SUCCESS");
    }
    else if (errortype == "Error") {
        toastr["error"](strmsg, "ERROR");
    }
    else if (errortype == "Info") {
        toastr["info"](strmsg, "INFORMATION");
    }
    else {
        toastr["error"](strmsg, "ERROR");
    }
}
// TABLE- WORKTYPE
var arrHead = new Array();	// array for header.
arrHead = ['', 'Work Type', 'Is architectural change?'];
// TABLE- WORKTYPE
var arrLaneRestrictions = new Array();	// array for header.
arrLaneRestrictions = ['', 'Lane Number', 'Restriction Type', 'Restriction Units', 'Restriction Value'];
var arrLaneTypes = new Array();	// array for header.
arrLaneTypes = ['Lane Number', 'Lane Type'];

function updateRestriction(element) {
    var restriction_type = element.value
    var types_no_value = ['notrucks', 'travelpeakhoursonly', 'hov3', 'hov2', 'noparking', 'towingprohibited', 'permittedoversizeloadsprohibitied']
    var types_distance_units = ['reducedwidth', 'reducedheight', 'reducedlength']
    var distance_units = ['feet', 'inches', 'centimeters']
    var distance_unit_names = ['ft', 'in', 'cm']
    var types_mass_units = ['reducedweight', 'axleloadlimit', 'grossweightlimit']
    var mass_units = ['pounds', 'tons', 'kilograms']
    var mass_unit_names = ['lbs', 'tons', 'kg']
    var units = []
    var unitNames = []
    var disabled = true
    if (types_distance_units.indexOf(restriction_type) >= 0) {
        units = distance_units
        unitNames = distance_unit_names
        disabled = false
    }
    else if (types_mass_units.indexOf(restriction_type) >= 0) {
        units = mass_units
        unitNames = mass_unit_names
        disabled = false
    }
    var tr = element.closest('tr');

    for (c = 0; c < tr.cells.length; c++) {
        var element = tr.cells[c];
        if (element.childNodes[0].id == 'restrictionvalue') {
            if (disabled) {
                element.childNodes[0].setAttribute('disabled', disabled)
                element.childNodes[0].value = ""
            }
            else {
                element.childNodes[0].removeAttribute('disabled')
            }
        }
        else if (element.childNodes[0].id == 'mySelectUnits') {
            var unit = element.childNodes[0].value;
            for (i = element.childNodes[0].options.length - 1; i >= 0; i--) {
                element.childNodes[0].options[i] = null;
            }
            for (var i = 0; i < units.length; i++) {
                var option = document.createElement("option");
                option.setAttribute('type', 'option');
                option.value = units[i];
                option.text = unitNames[i];
                element.childNodes[0].appendChild(option);
            }
            if (units.indexOf(unit) >= 0) element.childNodes[0].value = unit
        }

    }
    //var restriction_type = $(this).value;

}
// first create TABLE structure with the headers. 
function createTable() {
    var empTable = document.createElement('table');
    empTable.setAttribute('id', 'empTable'); // table id.

    var tr = empTable.insertRow(-1);
    for (var h = 0; h < arrHead.length; h++) {
        var th = document.createElement('th'); // create table headers
        th.innerHTML = arrHead[h];
        tr.appendChild(th);
    }

    var div = document.getElementById('cont');
    div.appendChild(empTable);  // add the TABLE to the container.
    document.getElementById("addRow").addEventListener("click", addRow);
    document.getElementById("bt").addEventListener("click", submitbtn);
}
function createTable_lanerestrictions() {
    var lanerestrictTable = document.createElement('table');
    lanerestrictTable.setAttribute('id', 'lanerestrictionTable'); // table id.

    var tr = lanerestrictTable.insertRow(-1);
    for (var h = 0; h < arrLaneRestrictions.length; h++) {
        var th = document.createElement('th'); // create table headers
        th.innerHTML = arrLaneRestrictions[h];
        tr.appendChild(th);
    }

    var div = document.getElementById('cont_LaneRestriction');
    div.appendChild(lanerestrictTable);  // add the TABLE to the container.
    document.getElementById("addRow_LaneRestriction").addEventListener("click", addRow_LaneRestriction);
    // document.getElementById("bt_LaneRestriction").addEventListener("click", submitbtn_LaneRestriction);
}
function createTable_lanetype() {
    //console.log("createing LANETYPE TABLE");
    var lanetypeTable = document.createElement('table');
    lanetypeTable.setAttribute('id', 'lanetypeTable'); // table id.

    var tr = lanetypeTable.insertRow(-1);
    for (var h = 0; h < arrLaneTypes.length; h++) {
        //console.log("CREATE LANETYPE -for log");
        var th = document.createElement('th'); // create table headers
        th.innerHTML = arrLaneTypes[h];
        tr.appendChild(th);
    }

    var div = document.getElementById('cont_LaneType');
    div.appendChild(lanetypeTable);  // add the TABLE to the container.
    //document.getElementById("addRow_LaneTypes").addEventListener("click", addRow_LaneType);
    // document.getElementById("bt_LaneRestriction").addEventListener("click", submitbtn_LaneRestriction);
}
fillTable();

// now, add a new to the TABLE - WORK TYPES.
function addRow() {
    var empTab = document.getElementById('empTable');

    var rowCnt = empTab.rows.length;   // table row count.
    var tr = empTab.insertRow(rowCnt); // the table row.
    tr = empTab.insertRow(rowCnt);

    for (var c = 0; c < arrHead.length; c++) {
        var td = document.createElement('td'); // table definition.
        td = tr.insertCell(c);

        if (c == 0) {      // the first column.
            // add a button in every new row in the first column.
            var button = document.createElement('input');

            // set input attributes.
            button.setAttribute('type', 'button');
            button.setAttribute('value', 'Remove');
            button.setAttribute('class', 'btnGridRemove');
            // add button's 'onclick' event.
            button.setAttribute('onclick', 'removeRow(this)');

            td.appendChild(button);
        }
        else if (c == 2) {
            var x = document.createElement("INPUT");
            x.setAttribute("type", "checkbox");
            td.appendChild(x);

        }
        else if (c == 1) {
            var ddl = document.getElementById('ddTypeOfWork');
            var newarray = new Array();
            for (i = 0; i < ddl.options.length; i++) {
                newarray[i] = ddl.options[i].value + ',' + ddl.options[i].text;
            }

            //Create and append select list
            var selectList = document.createElement("select");
            selectList.id = "mySelect";
            td.appendChild(selectList);
            for (var i = 0; i < newarray.length; i++) {
                var option = document.createElement("option");
                option.setAttribute('type', 'option');
                option.value = newarray[i].split(',')[0];
                option.text = newarray[i].split(',')[1];
                selectList.appendChild(option);
            }

        }
        else {
            // 2nd, 3rd and 4th column, will have textbox.

        }
    }
}

// delete TABLE row function.
function removeRow(oButton) {
    var empTab = document.getElementById('empTable');
    empTab.deleteRow(oButton.parentNode.parentNode.rowIndex); // button -> td -> tr.
}
function removeRow_lanerestriction(oButton) {
    var empTab = document.getElementById('lanerestrictionTable');
    empTab.deleteRow(oButton.parentNode.parentNode.rowIndex); // button -> td -> tr.
}


// function to extract and submit table data.
function submitbtn() {
    console.log('submitting')
    var myTab = document.getElementById('empTable');
    var arrValues = ""

    // loop through each row of the table.
    for (row = 1; row < myTab.rows.length - 1; row++) {
        // loop through each cell in a row.
        var selectedOption = "";
        var checkboxChecked = false;
        for (c = 0; c < myTab.rows[row].cells.length; c++) {
            var element = myTab.rows.item(row).cells[c];

            if (element.childNodes[0].id == 'mySelect') {
                var x = element.childNodes[0].selectedIndex;
                selectedOption = element.childNodes[0][x].value;
            }
            if (element.childNodes[0].getAttribute('type') == 'checkbox') {
                checkboxChecked = element.childNodes[0].checked;
            }
        }
        if (selectedOption.trim() == "") continue;
        arrValues += selectedOption + "," + checkboxChecked + ";";
        //console.log(arrValues)
    }
    arrValues = arrValues;

    document.getElementById('myHiddenoutputlist').value = arrValues;

    //Submit Lanerestriction table
    myTab = document.getElementById('lanerestrictionTable');
    var arrValues_lanerestrictions = "";

    console.log("Table Length: " + myTab.rows.length)
    for (row = 1; row < myTab.rows.length - 1; row++) {
        selectedOption = "";
        var selectedOption_2 = "";
        var lanenumber = "";
        var restrictionvalue = "";
        for (c = 0; c < myTab.rows[row].cells.length; c++) {
            var element = myTab.rows.item(row).cells[c];
            console.log("LaneRestriction Element: " + element);
            if (element.childNodes[0].id == 'laneno') {
                lanenumber = element.childNodes[0].value;
            }
            if ((element.childNodes[0].getAttribute('type') == 'text') && (element.childNodes[0].id == 'restrictionvalue')) {
                restrictionvalue = element.childNodes[0].value;
            }
            if (element.childNodes[0].id == 'mySelect') {
                var x = element.childNodes[0].selectedIndex;
                selectedOption = element.childNodes[0][x].value
            }
            if (element.childNodes[0].id == 'mySelectUnits' && element.childNodes[0].selectedIndex != -1) {
                var x = element.childNodes[0].selectedIndex;
                selectedOption_2 = element.childNodes[0][x].value;
            }

        }
        if ((selectedOption.trim() == "") && (lanenumber.trim() == "") && (selectedOption_2.trim() == "")) continue;
        arrValues_lanerestrictions += lanenumber + "," + selectedOption + "," + selectedOption_2 + "," + restrictionvalue + ";";
    }
    console.log("LaneRestrict: " + arrValues_lanerestrictions);
    document.getElementById('Hidden_list_LaneRestriction').value = arrValues_lanerestrictions;

    //Submit LaneType table
    myTab = document.getElementById('lanetypeTable');
    var arrValues_lanetypes = "";
    console.log('Processing Lane Type')
    //console.log("lanetype submit");
    for (row = 1; row < myTab.rows.length - 1; row++) {
        var selectedOption = "";
        lanenumber = "";
        for (c = 0; c < myTab.rows[row].cells.length; c++) {
            var element = myTab.rows.item(row).cells[c];
            if (element.childNodes[0].getAttribute('type') == 'text') {
                lanenumber = element.childNodes[0].value;
            }
            if (element.childNodes[0].id == 'mySelect') {
                var x = element.childNodes[0].selectedIndex;
                selectedOption = element.childNodes[0][x].value
            }

        }
        if ((selectedOption.trim() == "") && (lanenumber.trim() == "")) continue;
        arrValues_lanetypes += lanenumber + "," + selectedOption + ";";
    }
    console.log(arrValues_lanetypes)
    //console.log("LaneType: " + arrValues_lanetypes);
    document.getElementById('HiddenLaneType').value = arrValues_lanetypes;
}


// now, add a new to the TABLE - LANE RESTRICTIONS.
function addRow_LaneRestriction() {
    var lanerestrictTab = document.getElementById('lanerestrictionTable');

    var rowCnt = lanerestrictTab.rows.length;   // table row count.
    var tr = lanerestrictTab.insertRow(rowCnt); // the table row.
    tr = lanerestrictTab.insertRow(rowCnt);

    for (var c = 0; c < arrLaneRestrictions.length; c++) {
        var td = document.createElement('td'); // table definition.
        td = tr.insertCell(c);

        if (c == 0) {      // the first column.
            // add a button in every new row in the first column.
            var button = document.createElement('input');

            // set input attributes.
            button.setAttribute('type', 'button');
            button.setAttribute('value', 'Remove');
            button.setAttribute('class', 'btnGridRemove');
            // add button's 'onclick' event.
            button.setAttribute('onclick', 'removeRow_lanerestriction(this)');

            td.appendChild(button);
        }
        else if (c == 3) {
            var ddl = document.getElementById('ddRestrictionUnits');
            var newarray = new Array();
            for (i = 0; i < ddl.options.length; i++) {
                newarray[i] = ddl.options[i].value + ',' + ddl.options[i].text;
            }

            //Create and append select list
            var selectList = document.createElement("select");
            selectList.id = "mySelectUnits";
            td.appendChild(selectList);
            for (var i = 0; i < newarray.length; i++) {
                var option = document.createElement("option");
                option.setAttribute('type', 'option');
                option.value = newarray[i].split(',')[0];
                option.text = newarray[i].split(',')[1];
                selectList.appendChild(option);
            }

        }
        else if (c == 2) {
            var ddl = document.getElementById('ddRestrictionTypes');
            var newarray = new Array();
            for (i = 0; i < ddl.options.length; i++) {
                newarray[i] = ddl.options[i].value + ',' + ddl.options[i].text;
            }

            //Create and append select list
            var selectList = document.createElement("select");
            selectList.id = "mySelect";
            td.appendChild(selectList);
            for (var i = 0; i < newarray.length; i++) {
                var option = document.createElement("option");
                option.setAttribute('type', 'option');
                option.value = newarray[i].split(',')[0];
                option.text = newarray[i].split(',')[1];
                selectList.appendChild(option);
            }
            selectList.setAttribute('onchange', 'updateRestriction(this)');


        }
        else if (c == 1) {
            var laneSelect = document.createElement("select");
            laneSelect.id = 'laneno'
            td.appendChild(laneSelect);
            var ddnumberoflanes = document.getElementById("dd_numberoflanes");
            var numLanes = ddnumberoflanes.options[ddnumberoflanes.selectedIndex].value;
            for (i = 1; i <= numLanes; i++) {
                var option = document.createElement("option");
                option.setAttribute('type', 'option');
                option.value = i;
                option.text = i;
                laneSelect.appendChild(option);
            }
            //var ele = document.createElement('input');
            //ele.setAttribute('type', 'text');
            //ele.setAttribute('value', '');
            //ele.id = "laneno";
            //td.appendChild(ele);


        }
        else if (c == 4) {
            // 2nd, 3rd and 4th column, will have textbox.
            var ele = document.createElement('input');
            ele.setAttribute('type', 'text');
            ele.setAttribute('value', '');
            ele.id = "restrictionvalue";

            td.appendChild(ele);
        }
    }

}

function addPopulateRow(work_type, arch_change) {
    var empTab = document.getElementById('empTable');

    var rowCnt = empTab.rows.length;   // table row count.
    var tr = empTab.insertRow(rowCnt); // the table row.
    tr = empTab.insertRow(rowCnt);

    for (var c = 0; c < arrHead.length; c++) {
        var td = document.createElement('td'); // table definition.
        td = tr.insertCell(c);

        if (c == 0) {      // the first column.
            // add a button in every new row in the first column.
            var button = document.createElement('input');

            // set input attributes.
            button.setAttribute('type', 'button');
            button.setAttribute('value', 'Remove');
            button.setAttribute('class', 'btnGridRemove');
            // add button's 'onclick' event.
            button.setAttribute('onclick', 'removeRow(this)');

            td.appendChild(button);
        }
        else if (c == 2) {
            var x = document.createElement("INPUT");
            x.setAttribute("type", "checkbox");
            x.checked = (arch_change.toLowerCase() == "true")
            td.appendChild(x);

        }
        else if (c == 1) {
            var ddl = document.getElementById('ddTypeOfWork');
            var newarray = new Array();
            for (i = 0; i < ddl.options.length; i++) {
                newarray[i] = ddl.options[i].value + ',' + ddl.options[i].text;
            }

            //Create and append select list
            var selectList = document.createElement("select");
            selectList.id = "mySelect";
            td.appendChild(selectList);
            for (var i = 0; i < newarray.length; i++) {
                var option = document.createElement("option");
                option.setAttribute('type', 'option');
                option.value = newarray[i].split(',')[0];
                option.text = newarray[i].split(',')[1];
                selectList.appendChild(option);
            }
            selectList.value = work_type;

        }
        else {
            // 2nd, 3rd and 4th column, will have textbox.

        }
    }
}

function fillTable() {

    if (document.contains(document.getElementById("empTable"))) document.getElementById("empTable").remove();
    createTable()
    arrValuesText = document.getElementById('myHiddenoutputlist').value
    //console.log(arrValuesText);
    if (arrValuesText.trim() != "") {
        arrValues = arrValuesText.split(";");
        //console.log(arrValues);
        for (var i = 0; i < arrValues.length; i++) {
            //console.log(arrValues[i]);
            if (arrValues[i] == "'', ''" || arrValues[i] == "") continue;
            row = arrValues[i].split(",");
            //console.log(row[0].trim().replace("'", "") + ", " + row[1].trim().replace("'", ""))
            addPopulateRow(row[0].trim().replace("'", ""), row[1].trim().replace("'", ""));
        }
    }
    else addRow()
    if (document.contains(document.getElementById("lanerestrictionTable"))) document.getElementById("lanerestrictionTable").remove();
    createTable_lanerestrictions();
    //console.log("after tbl create");
    var arrValuesText_LR = document.getElementById('Hidden_list_LaneRestriction').value
    if (arrValuesText_LR.trim() != "") {
        arrValues = arrValuesText_LR.split(";");
        //console.log(arrValues);
        for (var i = 0; i < arrValues.length; i++) {
            //console.log(arrValues[i]);
            if (arrValues[i] == "'', ''" || arrValues[i] == "") continue;
            row = arrValues[i].split(",");
            //console.log(row[0].trim().replace("'", "") + ", " + row[1].trim().replace("'", "") + row[2].trim().replace("'", ""))
            addPopulateRow_LaneRestrictions(row[0].trim().replace("'", ""), row[1].trim().replace("'", ""), row[2].trim().replace("'", ""), row[3].trim().replace("'", ""));

        }
    }
    else addRow_LaneRestriction()

    if (document.contains(document.getElementById("lanetypeTable"))) document.getElementById("lanetypeTable").remove();

    createTable_lanetype();
    //console.log("after tbl create");
    var arrValuesText_LT = document.getElementById('HiddenLaneType').value
    if (arrValuesText_LT.trim() != "") {
        arrValues = arrValuesText_LT.split(";");
        //console.log(arrValues);
        for (var i = 0; i < arrValues.length; i++) {
            //console.log(arrValues[i]);
            if (arrValues[i] == "'', ''" || arrValues[i] == "") continue;
            row = arrValues[i].split(",");
            //console.log(row[0].trim().replace("'", "") + ", " + row[1].trim().replace("'", "") )
            addPopulateRow_LaneTypes(row[0].trim().replace("'", ""), row[1].trim().replace("'", ""));
        }
    }
    else initLaneType();

    updateMarkers();
}
function addPopulateRow_LaneRestrictions(laneno, lane_restrictions, lane_units, restrictionvalue) {
    var empTab = document.getElementById('lanerestrictionTable');

    var rowCnt = empTab.rows.length;   // table row count.
    var tr = empTab.insertRow(rowCnt); // the table row.
    tr = empTab.insertRow(rowCnt);
    var restrictionTypeSelect;
    for (var c = 0; c < arrLaneRestrictions.length; c++) {
        var td = document.createElement('td'); // table definition.
        td = tr.insertCell(c);

        if (c == 0) {      // the first column.
            // add a button in every new row in the first column.
            var button = document.createElement('input');

            // set input attributes.
            button.setAttribute('type', 'button');
            button.setAttribute('value', 'Remove');
            button.setAttribute('class', 'btnGridRemove');
            // add button's 'onclick' event.
            button.setAttribute('onclick', 'removeRow_lanerestriction(this)');

            td.appendChild(button);
        }
        else if (c == 2) {
            var ddl = document.getElementById('ddRestrictionTypes');
            var newarray = new Array();
            for (i = 0; i < ddl.options.length; i++) {
                newarray[i] = ddl.options[i].value + ',' + ddl.options[i].text;
            }

            //Create and append select list
            var selectList = document.createElement("select");
            selectList.id = "mySelect";
            td.appendChild(selectList);
            for (var i = 0; i < newarray.length; i++) {
                var option = document.createElement("option");
                option.setAttribute('type', 'option');
                option.value = newarray[i].split(',')[0];
                option.text = newarray[i].split(',')[1];
                selectList.appendChild(option);
            }
            restrictionTypeSelect = selectList;
            selectList.setAttribute('onchange', 'updateRestriction(this)');
            selectList.value = lane_restrictions;

        }
        else if (c == 1) {
            //lane no
            var laneSelect = document.createElement("select");
            laneSelect.id = "laneno";
            td.appendChild(laneSelect);
            var ddnumberoflanes = document.getElementById("dd_numberoflanes");
            var numLanes = ddnumberoflanes.options[ddnumberoflanes.selectedIndex].value;
            for (i = 1; i <= numLanes; i++) {
                var option = document.createElement("option");
                option.setAttribute('type', 'option');
                option.value = i;
                option.text = i;
                laneSelect.appendChild(option);
            }
            laneSelect.value = laneno;
        }
        else if (c == 3) {
            //console.log("c=3");
            var ddl = document.getElementById('ddRestrictionUnits');
            var newarray = new Array();
            for (i = 0; i < ddl.options.length; i++) {
                newarray[i] = ddl.options[i].value + ',' + ddl.options[i].text;
            }

            //Create and append select list
            var selectList = document.createElement("select");
            selectList.id = "mySelectUnits";
            td.appendChild(selectList);
            for (var i = 0; i < newarray.length; i++) {
                var option = document.createElement("option");
                option.setAttribute('type', 'option');
                option.value = newarray[i].split(',')[0];
                option.text = newarray[i].split(',')[1];
                selectList.appendChild(option);
            }
            //console.log(lane_units);
            selectList.value = lane_units;

        }
        else if (c == 4) {
            //lane no
            var ele = document.createElement('input');
            ele.setAttribute('type', 'text');
            ele.setAttribute('value', '');
            ele.value = restrictionvalue;
            ele.id = "restrictionvalue";
            td.appendChild(ele);
        }
        else {
            // 2nd, 3rd and 4th column, will have textbox.

        }
    }
    updateRestriction(restrictionTypeSelect)
}

function addPopulateRow_LaneTypes(laneno, lane_type) {
    var empTab = document.getElementById('lanetypeTable');

    var rowCnt = empTab.rows.length;   // table row count.
    var tr = empTab.insertRow(rowCnt); // the table row.
    tr = empTab.insertRow(rowCnt);

    for (var c = 0; c < arrLaneTypes.length; c++) {
        var td = document.createElement('td'); // table definition.
        td = tr.insertCell(c);
        if (c == 1) {
            var ddl = document.getElementById('ddLaneTypes');
            var newarray = new Array();
            for (i = 0; i < ddl.options.length; i++) {
                newarray[i] = ddl.options[i].value + ',' + ddl.options[i].text;
            }

            //Create and append select list
            var selectList = document.createElement("select");
            selectList.id = "mySelect";
            td.appendChild(selectList);
            for (var i = 0; i < newarray.length; i++) {
                var option = document.createElement("option");
                option.setAttribute('type', 'option');
                option.value = newarray[i].split(',')[0];
                option.text = newarray[i].split(',')[1];
                selectList.appendChild(option);
            }
            selectList.value = lane_type;
        }
        else if (c == 0) {
            //lane no
            var ele = document.createElement('input');
            ele.setAttribute('type', 'text');
            ele.setAttribute('value', '');
            ele.setAttribute('disabled', 'true');
            ele.value = laneno;
            td.appendChild(ele);
            

        }
        else {
            // 2nd, 3rd and 4th column, will have textbox.

        }
    }
}
function initLaneType() {
    //set vehiclepathdropdown items
    var ddnumberoflanes = document.getElementById("dd_numberoflanes");
    var ddnumberoflanes_val = ddnumberoflanes.options[ddnumberoflanes.selectedIndex].value;
    var ddnumberoflanes_vechiledatapath = document.getElementById("dd_avgvehicledatapath");
    ////clear items in dropdown
    ddnumberoflanes_vechiledatapath.options.length = 0;
    for (i = 1; i <= ddnumberoflanes_val; i++) {
        var opt = document.createElement("option");
        opt.text = i;
        opt.value = i;
        ddnumberoflanes_vechiledatapath.options.add(opt);
        //if (i == ddnumberoflanes_val)
        //    ddnumberoflanes_vechiledatapath.options[i].selected = true;
    }
    // var lane_edge_reference = 'left'
    if (document.contains(document.getElementById("lanetypeTable"))) document.getElementById("lanetypeTable").remove();
    createTable_lanetype();
    var lane_type;
    var num_lanes = document.getElementById('dd_numberoflanes').value
    for (i = 1; i <= num_lanes; i++) {
        lane_type = 'middlelane' //left-lane, right-lane, middle-lane, right-exit-lane, left-exit-lane, ... (exit lanes, merging lanes, turning lanes)
        if (i == 1 && num_lanes > 1) lane_type = 'leftlane'
        else if (i == num_lanes && num_lanes > 1) lane_type = 'rightlane'
        addPopulateRow_LaneTypes(i, lane_type)
    }

    myTab = document.getElementById('lanerestrictionTable');

    for (row = 1; row < myTab.rows.length - 1; row++) {
        for (c = 0; c < myTab.rows[row].cells.length; c++) {
            var element = myTab.rows.item(row).cells[c];
            if (element.childNodes[0].id == 'laneno') {
                var laneSelect = element.childNodes[0];
                var val = laneSelect.options[laneSelect.selectedIndex].value;
                laneSelect.options.length = 0;
                for (i = 1; i <= ddnumberoflanes_val; i++) {
                    var option = document.createElement("option");
                    option.setAttribute('type', 'option');
                    option.value = i;
                    option.text = i;
                    laneSelect.appendChild(option);
                }
                if (val <= ddnumberoflanes_val) laneSelect.value = val;
            }
        }
    }
}