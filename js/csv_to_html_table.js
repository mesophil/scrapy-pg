var CsvToHtmlTable = CsvToHtmlTable || {};

CsvToHtmlTable = {
    init: function (options) {
        options = options || {};
        var csv_path = options.csv_path || "";
        var el = options.element || "table-container";
        var allow_download = options.allow_download || false;
        var csv_options = options.csv_options || {};
        var datatables_options = options.datatables_options || {};
        var custom_formatting = options.custom_formatting || [];
        var customTemplates = {};
        $.each(custom_formatting, function (i, v) {
            var colIdx = v[0];
            var func = v[1];
            customTemplates[colIdx] = func;
        });

        var $table = $("<table class='table table-striped table-condensed' id='" + el + "-table'></table>");

        var $containerElement = $("#" + el);
        $containerElement.empty().append($table);

        $.when($.get(csv_path)).then(
            function (data) {
                var csvData = $.csv.toArrays(data, csv_options);
                var $tableHead = $("<thead></thead>");
                var csvHeaderRow = csvData[0];
                var $tableHeadRow = $("<tr></tr>");
                for (var headerIdx = 0; headerIdx < csvHeaderRow.length; headerIdx++) {
                    $tableHeadRow.append($("<th></th>").text(csvHeaderRow[headerIdx]));
                }
                $tableHead.append($tableHeadRow);

                $table.append($tableHead);
                var $tableBody = $("<tbody></tbody>");

                for (var rowIdx = 1; rowIdx < csvData.length; rowIdx++) {
                    var $tableBodyRow = $("<tr></tr>");
                    for (var colIdx = 0; colIdx < csvData[rowIdx].length; colIdx++) {
                        var $tableBodyRowTd = $("<td></td>");
                        var cellTemplateFunc = customTemplates[colIdx];
                        if (cellTemplateFunc) {
                            $tableBodyRowTd.html(cellTemplateFunc(csvData[rowIdx][colIdx]));
                        } else {
                            $tableBodyRowTd.text(csvData[rowIdx][colIdx]);
                        }
                        $tableBodyRow.append($tableBodyRowTd);
                        $tableBody.append($tableBodyRow);
                    }
                }
                $table.append($tableBody);

                if (datatables_options.dom) {
                    // If dom is already specified, ensure it includes pagination at top and bottom
                    if (datatables_options.dom.indexOf('p') === -1) {
                        datatables_options.dom = 'p' + datatables_options.dom + 'p';
                    } else if (datatables_options.dom.indexOf('p') === datatables_options.dom.lastIndexOf('p')) {
                        // Only one 'p', add another at the beginning
                        datatables_options.dom = 'p' + datatables_options.dom;
                    }
                } else {
                    datatables_options.dom = 'pfrtip'; // p=pagination, f=filter, r=processing, t=table, i=info
                }

                $table.DataTable(datatables_options);

                var $inputRow = $('<tr></tr>');

                $table.DataTable().columns().every(function (index) {
                    if (!([4, 5, 6, 10].includes(index))) {
                        var column = this;
                        var header = $(column.header());
                        var $inputCell = $('<td></td>');

                        var input = $('<input type="text" placeholder="..." class="form-control form-control-sm" style="max-width: 10em"/>')
                            .appendTo($inputCell)
                            .on('keydown', function (e) {
                                if(e.type === 'keydown' && e.keyCode === 13){
                                    e.preventDefault();
                                    column.search($(this).val()).draw();
                                }
                            });

                        $inputCell.appendTo($inputRow);

                    } else {
                        var $regularCell = $('<td></td>');
                        $regularCell.appendTo($inputRow);
                    }

                    $inputRow.appendTo($table.DataTable().table().header());
                });

                if (allow_download) {
                    $containerElement.append("<p><a class='btn btn-info' href='" + csv_path + "'><i class='glyphicon glyphicon-download'></i> Download as CSV</a></p>");
                }
            });
    }
};