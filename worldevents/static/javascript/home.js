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
	
	//delete messages
	delete_messages()

	//toggle map/detail link
	toggle_map_detail()

	//back to list link
	back_to_list()
	}

function first_lng(){
return $("tr:first").find("td:eq(1)").html().substring($("tr:first").find("td:eq(1)").html().lastIndexOf(",")+1,$("tr:first").find("td:eq(1)").html().indexOf("]"))
}

function first_lat(){
return $("tr:first").find("td:eq(1)").html().substring($("tr:first").find("td:eq(1)").html().indexOf("[")+1,$("tr:first").find("td:eq(1)").html().lastIndexOf(","))
}

function create_map_detail(lat,lng){
$("#map_detail").gmap3({
          map:{
            options:{
              center:[lat,lng],
              zoom: 8
            }
          }
        });
}

function set_first_event(){
$("tr:first").addClass("selected_event")
	id=($(".selected_event").find("td:first").html())
	$("#"+id).toggle()
}

function toggle_comments_form(){
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


function show_form(){
$(".form").on("click",function(e){
		e.preventDefault()
		$("#form_container").load($(this).attr("href"),function(){
		show_form_container()
		});
		
		
	});
}

function process_comment_form(){
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

		$("#"+id).toggle()
		$(".selected_event").removeClass("selected_event")
		$(this).addClass("selected_event")
		id=($(this).find("td:first").html())
		$("#"+id).toggle()
		lat=$(this).find("td:eq(1)").html().substring($(this).find("td:eq(1)").html().indexOf("[")+1,$(this).find("td:eq(1)").html().lastIndexOf(","))
		lng=$(this).find("td:eq(1)").html().substring($(this).find("td:eq(1)").html().lastIndexOf(",")+1,$(this).find("td:eq(1)").html().indexOf("]"))
		map.gmap3({clear:{tag:[id]}});
		addMarker(map,id,red_icon,lat,lng)
		map.gmap3("get").setCenter(new google.maps.LatLng(lat,lng))

		if ($(window).width()<800){
			$("#events_list").css("width","0px")
			$("#events_list").css("height","0px")
			$("#events_list").css("overflow","hidden")
			$(".event_detail").css("width","100%")
			$(".event_detail").css("height","auto")
			$("#toggle_map_detail").css("display","block")
			$("#back_to_list").css("display","block")
		}

	});
}


function delete_messages(){
	$("#messages").fadeOut(5000, "linear",function(){
		$(".messages").remove()
	});

}



function toggle_map_detail(){
	$("#toggle_map_detail").click(function(){
		detail=$(".event_detail")
		map=$("#map_detail")
		if ($(window).width()<800){
			width="100%"
		}else{
			width="50%"
		}
		if (detail.width()<=1){
			detail.css("width",width)
			detail.css("height","auto")
			map.css("width","0px")
			map.css("height","0px")
		}else{
			detail.css("width","0px")
			detail.css("height","0px")
			map.css("width",width)
			map.css("height","300px")
			map.gmap3({trigger:"resize"});
			center_map()
		}
		
	});

}


function back_to_list(){
	$("#back_to_list").click(function(){
		detail=$(".event_detail")
		map=$("#map_detail")
		events_list=$("#events_list")
		detail.css("width","0px")
		detail.css("height","0px")
		map.css("width","0px")
		map.css("height","0px")
		events_list.css("width","100%")
		events_list.css("height","auto")
		$("#back_to_list").css("display","none")
		$("#toggle_map_detail").css("display","none")
	});	
}

function addMarkers(){
		map=$("#map_detail")
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
	{	
		$("body").append("<div id='shade'></div>")
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


	function center_map()
	{

		map=$("#map_detail")
		id=($(".selected_event").find("td:first").html())
		lat=$(".selected_event").find("td:eq(1)").html().substring($(".selected_event").find("td:eq(1)").html().indexOf("[")+1,$(".selected_event").find("td:eq(1)").html().lastIndexOf(","))
		lng=$(".selected_event").find("td:eq(1)").html().substring($(".selected_event").find("td:eq(1)").html().lastIndexOf(",")+1,$(".selected_event").find("td:eq(1)").html().indexOf("]"))
		map.gmap3("get").setCenter(new google.maps.LatLng(lat,lng))

	}	












