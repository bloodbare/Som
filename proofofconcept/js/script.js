/* Author: 

*/
$(function(){

        // Tabs
        $('#tabs').tabs().find( ".ui-tabs-nav" ).sortable({
            axis: "x",
            connectWith: ".cell",
            placeholder: 'ui-sortable-placeholder2' });
        
		$( ".cell" ).sortable({
			connectWith: [".cell",".ui-tabs-nav"]
		});

		$( ".portlet" ).addClass( "ui-widget ui-widget-content ui-helper-clearfix ui-corner-all" )
			.find( ".portletHeader" )
				.addClass( "ui-widget-header ui-corner-all" )
				.prepend( "<span class='ui-icon ui-icon-minusthick'></span>")
				.end()
			.find( ".portletContent" );

		$( ".portletHeader .ui-icon" ).click(function() {
			$( this ).toggleClass( "ui-icon-minusthick" ).toggleClass( "ui-icon-plusthick" );
			$( this ).parents( ".portlet:first" ).find( ".portletContent" ).toggle();
		});

		$( ".cell" ).disableSelection();
		
		function addTab() {
			var tab_title = $tab_title_input.val() || "Tab " + tab_counter;
			$tabs.tabs( "add", "#tabs-" + tab_counter, tab_title );
			tab_counter++;
		}

});




















