function changeSelect(){
    var topic = $('#topic');
    var sub_topic = $('#subscribe_topic');
    var selectVal = $('#pubDevice option:selected').val();
    topic.val(selectVal);
    var sub = (selectVal=='')? '':selectVal+"_result";
    sub_topic.val(sub);
  }
  
function changeQueueSelect(){
  var selectVal = $('#regQueue option:selected').val();
  getList("registerQueue/"+selectVal,httpRequest3);
}
  
function changeMsg(){
  $('#optionMessage').val('');
  var option = $('#message').val();
  if(option==='remove'){
    var objectSel = $('#object').removeAttr('disabled'); 
  }
  else{
    var objectSel = $('#object').attr("disabled","disabled"); 
  }
}
  
function getList(requestName,httpRequest){
  httpRequest = new XMLHttpRequest();
  httpRequest.onreadystatechange = function(){
    printList(httpRequest);
  };

  if(!httpRequest){
      console.log("Can't make XMLHTTP instance");
      return false;
  }

  httpRequest.open('GET',requestName);
  httpRequest.send();
}
  
function printList(httpRequest){
  try{
      if(httpRequest.readyState === XMLHttpRequest.DONE){
          if(httpRequest.status === 200){
            console.log(httpRequest.responseURL);
            var url = httpRequest.responseURL;
            printListDetail(url,httpRequest);
          }
      }
  }
  catch(e){
    console.log(e.message);
    //print(e.message);
  }
}
  
function printListDetail(url,httpRequest){
  if(url.endsWith("devices")){
    var list = JSON.parse(httpRequest.responseText);
    var deviceList = $('#pubDevice');
    deviceList.empty();
    deviceList.append("<option value='' selected disabled >Select a device</option>");
    for(var count = 0; count < list.length; ++count){
      //console.log(list[count]);
      deviceList.append("<option value='"+list[count]["name"]+"'>"
      +list[count]["name"]+'_'+list[count]["_id"]+"</option>");
    }
    var deviceNum = $('#deviceNum');
    deviceNum.val(list.length+1);
    changeSelect();
  }
  
  else if(url.endsWith("registerQueue")){
    var list = JSON.parse(httpRequest.responseText);
    var deviceList = $('#regQueue');
    deviceList.empty();
    deviceList.append("<option value='' selected disabled >Select a device</option>");
    for(var count = 0; count < list.length; ++count){
      deviceList.append("<option value='"+list[count]["name"]+"'>"
      +list[count]["name"]+"</option>");
      }
    //changeSelect();
  }
    // GET 
  else if(url.indexOf("/registerQueue/")>0){
    // hostname osname cpus ipAddr 
    var list = JSON.parse(httpRequest.responseText);
    var hostname = $('#hostname');
    hostname.val(list["hostname"]);
    var osname = $('#osname');
    osname.val(list["os_system"]);
    var cpus = $('#cpus');
    cpus.val(list["cpu_count"]);
    var ipAddr = $('#ipAddr');
    ipAddr.val(list["ipv4Addr"]);
  }
  else if(url.indexOf("/removeQueue/")>0){
    getList("registerQueue",httpRequest2);
    getList("devices",httpRequest1);
  }
}
  