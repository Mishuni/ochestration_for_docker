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
    $('#object').removeAttr('disabled'); 
  }
  else{
    $('#object').attr("disabled","disabled"); 
  }
}

function changeConn(name,connect){
  var xhr = new XMLHttpRequest();
  xhr.onload = function(){
    console.log(name," changed the connection to ",connect);
  };

  if(!xhr){
      console.log("Can't make XMLHTTP instance");
      return false;
  }

  xhr.open('PUT','connected/'+name,true);
  xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
  xhr.send('{"connected":"'+connect+'"}');
}
  
function getList(requestName,httpRequest){
  httpRequest = new XMLHttpRequest();
  httpRequest.onload = function(){
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
    var deviceTable=$('#deviceTable');
    deviceList.empty();
    deviceTable.empty();
    var headline = '<div class="row2 header"><div class="cell">No.</div>'+
    '<div class="cell">DEVICE NAME</div><div class="cell">IP ADDRESS</div><div class="cell">CPU</div>'+
    '<div class="cell">REGISTER DATE</div><div class="cell">HOSTNAME</div><div class="cell">OS</div>'+
    '<div class="cell">CONNECTED</div></div>';
    deviceTable.append(headline);
    deviceList.append("<option value='' selected disabled >Select a device</option>");
    devicesNameList=[];
    for(var count = 0; count < list.length; ++count){

      deviceList.append("<option value='"+list[count]["name"]+"'>"
      +list[count]["name"]+"</option>");
     
      var date = new Date(list[count]["register"].$date);
      var tableRow = 
      '<div class="row2"><div class="cell" data-title="No.">'+list[count]["_id"]+
      '</div><div class="cell" data-title="DEVICE NAME">'+list[count]["name"]+
      '</div><div class="cell" data-title="IP ADDRESS">'+list[count]["ipv4Addr"]+
      '</div><div class="cell" data-title="CPU">'+list[count]["cpu_count"]+
      '</div><div class="cell" data-title="REGISTER DATE">'+date_to_str(date)+
      '</div><div class="cell" data-title="HOSTNAME">'+list[count]["hostname"]+
      '</div><div class="cell" data-title="OS">'+list[count]["os_system"]+'</div>' ; 
      
      var lastLine = (list[count]["connected"])? 
      '<div class="cell" data-title="CONNECTED" style="color:#ff1a1a;">True</div></div>':
      '<div class="cell" data-title="CONNECTED">False</div></div>';

      deviceTable.append(tableRow+lastLine);      
      devicesNameList.push(list[count]["name"]);
   
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

function date_to_str(format)
{
    var year = format.getFullYear();
    var month = format.getMonth() + 1;
    if(month<10) month = '0' + month;
    var date = format.getDate();
    if(date<10) date = '0' + date;
    var hour = format.getHours();
    if(hour<10) hour = '0' + hour;
    var min = format.getMinutes();
    if(min<10) min = '0' + min;
    var sec = format.getSeconds();
    if(sec<10) sec = '0' + sec;

    return year + "-" + month + "-" + date + " " + hour + ":" + min + ":" + sec; 
}
  