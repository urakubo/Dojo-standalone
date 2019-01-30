
var editCheck1 = function(cell){
	var data = cell.getRow().getData();
	APP.removeMarker(data.id);
	cell.getRow().delete();
}

var ObjMarkerTable = new Tabulator("#MarkerTable", {
	layout:"fitColumns",      //fit columns to width of table
	autoResize:true,
	responsiveLayout:"hide",  //hide columns that dont fit on the table
	tooltips:true,            //show tool tips on cells
	addRowPos:"top",          //when adding a new row, add it to the top of the table
	history:true,             //allow undo and redo actions on the table
	pagination:"local",       //paginate the data
	paginationSize:10,         //allow 7 rows per page of data
	resizableRows:true,       //allow row order to be changed
	initialSort:[             //set the initial sort order of the data
		{column:"id", dir:"dsc"},
	],
	columns:[                 //define the table columns
		{title:"Delete", formatter:"buttonCross", width:80, align:"center", editor:"tickCross", editable:editCheck1},
		{title:"ID", field:"id", width:40},
		{title:"Name", field:"name", editor:"input"},
		{title:"Parent ID", field:"parentid"},
		{title:"Radius", field:"radius", width:40, align:"right", editor:"number",editorParams:{min:0.2, max:24, step:0.2}},
		{title:"R", field:"r", width:40, align:"right", editor:"range",editorParams:{min:0, max:255, step:1}},
		{title:"G", field:"g", width:40, align:"right", editor:"range",editorParams:{min:0, max:255, step:1}},
		{title:"B", field:"b", width:40, align:"right", editor:"range",editorParams:{min:0, max:255, step:1}},
	],
	
	
	// セルが編集されたとき
    cellEdited: function(cell) {
      // 渡ってくるパラメータcellについて: http://tabulator.info/docs/4.1/components#component-cell
      // 編集後の値
      var cellValue = cell.getValue();
      // 編集前の値
      var cellOldValue = cell.getOldValue();
      // 編集対象のセルがある列
      var row = cell.getRow();
      var act = row.getData().act;
      var id  = row.getData().id;
      var radius  = row.getData().radius;
      var r   = row.getData().r;
      var g   = row.getData().g;
      var b   = row.getData().b;
      var columnField = cell.getColumn().getField();

	  if(columnField == 'radius') {
			APP.changeMarkerRadius(id, radius);
		}
	  if(columnField == 'r' || columnField == 'g' || columnField == 'b') {
			APP.changeMarkerColor(id, r*256*256+g*256+b*1);
		}
    }
});


$("a#download_CSV_all").click(function (e) {
    e.stopPropagation();
    e.preventDefault();
    $.ajax({
        url: '/ws_to_fetch_all_data/',
    }).done(function (data) {
        // store the whole data into a global variable
        allData = data.data;
        $("div.tabulator").tabulator("download", "xlsx", "data.xlsx");
    });
});


 
