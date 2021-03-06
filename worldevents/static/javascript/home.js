red_icon="http://maps.google.com/mapfiles/ms/icons/red-dot.png"	  
blue_icon="http://maps.google.com/mapfiles/ms/icons/blue-dot.png"

function init() {
	//Select first event and show detail
	set_first_event()	

	//Create map and center in first event
	create_map_detail(first_lat(),first_lng())

	//Add pointers in the map	
	addMarkers()
	
	//Show or hide comments form
	toggle_comments_form()

	//show form 
	show_form()
	
	//process comment form
	process_comment_form()
	
	//process event form
	process_event_form()
	
	//change event detail
	changeEvent()
	
	//process search links	
	process_search_links()
	}

function first_lng(){
return $("tr:first").find("td:eq(1)").html().substring($("tr:first").find("td:eq(1)").html().lastIndexOf(",")+1,$("tr:first").find("td:eq(1)").html().indexOf("]"))
}

function first_lat(){
return $("tr:first").find("td:eq(1)").html().substring($("tr:first").find("td:eq(1)").html().indexOf("[")+1,$("tr:first").find("td:eq(1)").html().lastIndexOf(","))
}

function create_map_detail(lat,lng){
	if (!$('#map_detail').html().trim()){
		$("#map_detail").gmap3({
			  map:{
			    options:{
			      center:[lat,lng],
			      zoom: 8
			    }
			  }
			});
	}
}

function set_first_event(){
	$("tr:first").addClass("selected_event")
	if (($("td:nth-child(5)")).css("display")=='none'){
		id=($(".selected_event").find("td:first").html())
		$("#"+id).toggle()
	}
}

function toggle_comments_form(){
$("a[href='comment']").unbind("click")
$("a[href='comment']").on("click",function(e){
		e.preventDefault()
		if ($(this).text()=="Add comment"){
			$(this).text("Close")
			$(".event_detail[style='display: block;'] form").show()
			
		}else{
			$(this).text("Add comment")
			$(".event_detail[style='display: block;'] form").hide()
		}
		
	});
}

function process_search_links(){
$("a[href*='searchevents/']").unbind("click")
//Solo selecciono los enlaces de navegación de la lista, no el enlace del formulario de busqueda(/)
$("a[href*='searchevents/']").on("click",function(e){
		e.preventDefault()
		$.get( $(this).attr("href"), function( data ) {
			$("#events_list").remove()
			$("#togglemapdetail").remove()
			$(".event_detail").remove()
			$("#container").prepend(data)
			init()
		});	
		
		
	});
}

function show_form(){
$(".form").unbind("click")
$(".form").on("click",function(e){
		e.preventDefault()
		$("#form_container").load($(this).attr("href"),function(){
		show_form_container()
		});
		
		
	});
}

function process_comment_form(){
	$("ul.event_detail").unbind("submit")
	$("ul.event_detail").on("submit","form",function(e){
		e.preventDefault();
		var postData = new FormData()
		
		$("textarea",this).add("input:not([type='submit'])",this).each(function(i) {
        		postData.append($(this).attr("name"), $(this).val());
		});
		postData.append("event_id",$("ul.event_detail[style='display: block;']").attr("id"))

		var formUrl = $(this).attr("action");

		$.ajax({
			url:formUrl,
			type:"POST",
			data:postData,
			processData: false,
			contentType: false,
			success:function(data,textStatus,jqXHR)
			{
				
				$("ul.event_detail[style='display: block;'] .comments").html(data);
			},
			error:function(jqXHR,textStatus,errorThrown)
			{alert(errorThrown)}
		});
	});
}



function process_event_form(){
	$("#form_container").unbind("submit")
	$("#form_container").on("submit","form",function(e){
		e.preventDefault();
		//var postData = $(this).serializeArray();
		var postData = new FormData()
		$("#form_container form input[type='file']").each(function(i) {
			postData.append($(this).attr("name"), $(this).get(0).files[0]);
		});
		//postData.append("photo", $('#id_photo').get(0).files[0]);

    $("form textarea, form select, form input:not([type='submit']):not([name='photo'])").each(function(i) {
        postData.append($(this).attr("name"), $(this).val());
	
    });
	
		var formUrl = $(this).attr("action");
		$.ajax({
			url:formUrl,
			type:"POST",
			data:postData,
			processData: false,
			contentType: false,
			success:function(data,textStatus,jqXHR)
			{
				if (data.indexOf("<html>")!=-1){
					document.write(data)
					document.close()
					
				}else if (data.indexOf('<div id="events_list">')!=-1){
					$("#events_list").remove()
					$(".event_detail").remove()
					$("#container").prepend(data)
					$("#shade").remove();
					$("#form_container").html("");
					process_search_links()	
				}else{
					$("#form_container").html(data);
					show_close_link()
				}
			},
			error:function(jqXHR,textStatus,errorThrown)
			{}
		});
		e.unBind();
	});
}

function changeEvent(){
	$("tr").click(function(){
		map=$("#map_detail")
		id=($(".selected_event").find("td:first").html())
		lat=$(".selected_event").find("td:eq(1)").html().substring($(".selected_event").find("td:eq(1)").html().indexOf("[")+1,$(".selected_event").find("td:eq(1)").html().lastIndexOf(","))
		lng=$(".selected_event").find("td:eq(1)").html().substring($(".selected_event").find("td:eq(1)").html().lastIndexOf(",")+1,$(".selected_event").find("td:eq(1)").html().indexOf("]"))
		map.gmap3({clear:{tag:[id]}});
		addMarker(map,id,blue_icon,lat,lng)
		
		$("a[href='comment']").text("Add comment")
		$("#"+id+" form").hide()
		hidden=false
		if ($("#"+id).css('display') == 'none'){
			hidden=true
		}
		$("#"+id).hide()
		$(".selected_event").removeClass("selected_event")
		$(this).addClass("selected_event")
		id=($(this).find("td:first").html())
		if (!hidden){
			$("#"+id).show()
		}
		lat=$(this).find("td:eq(1)").html().substring($(this).find("td:eq(1)").html().indexOf("[")+1,$(this).find("td:eq(1)").html().lastIndexOf(","))
		lng=$(this).find("td:eq(1)").html().substring($(this).find("td:eq(1)").html().lastIndexOf(",")+1,$(this).find("td:eq(1)").html().indexOf("]"))
		map.gmap3({clear:{tag:[id]}});
		addMarker(map,id,red_icon,lat,lng)
		map.gmap3("get").setCenter(new google.maps.LatLng(lat,lng))
	});
}


function addMarkers(){
		map=$("#map_detail")
		map.gmap3({clear:{name:"marker"}});
		$("tr").each(function(){
			
			lat=$(this).find("td:eq(1)").html().substring($(this).find("td:eq(1)").html().indexOf("[")+1,$(this).find("td:eq(1)").html().lastIndexOf(","))
			lng=$(this).find("td:eq(1)").html().substring($(this).find("td:eq(1)").html().lastIndexOf(",")+1,$(this).find("td:eq(1)").html().indexOf("]"))
			if ($(this).hasClass("selected_event")){	
				icon_image=red_icon		
			}else{
				icon_image=blue_icon
			}
			tag_label=($(this).find("td:first").html())
			
			addMarker(map,tag_label,icon_image,lat,lng)
		});	
	}


	function addMarker(map,tag_label,icon_image,lat,lng){
		map.gmap3({
				marker:{
					latLng:[lat,lng],
					tag:tag_label,
					options:{
						draggable:true,
						icon: icon_image
					}
				}
		});
	}

	function show_form_container()
	{	$("body").append("<div id='shade'></div>")
		$("#form_container").css("display","block")
		show_close_link()
		$("input[value='Cancel']").click(function(){
			$("#shade").remove();
			$("#form_container").html("");
		});	
		
	}

	function show_close_link()
	{
		$("#form_container").append("<div class='close'><a href='#'>X</a></div>");
		$(".close").click(function(){
			$("#shade").remove();
			$("#form_container").html("");
		});	
	}

