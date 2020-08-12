$(window).load(function () {
  const ackInterval = 2000;
  let count = 0;
  let devicesNameList=[];
  let devicesNameList_copy=[];
  let httpRequest1,httpRequest2,httpRequest3;

  var socket = io.connect('http://' + document.domain + ':' + location.port);
  
  getList("devices",httpRequest1);
  getList("registerQueue",httpRequest2);

  // === Strat checking for MQTT connection ===
  setInterval(function(){
    console.log(count)
    if(count==1){
      var data = '{"topic": "ACK", "message": "ack"}';
      devicesNameList_copy = devicesNameList.slice();
      console.log(devicesNameList_copy);
      socket.emit('ack', data=data);
      count += 1;
    }
    else if(count==5){
      // make remaining devices's connection to False
      devicesNameList_copy.forEach(element => changeConn(element,"False"));
      getList("devices",httpRequest1);
      getList("registerQueue",httpRequest2);
      count = 0;
    }
    else{
      count += 1;
    }
  },ackInterval);
  // === End checking for MQTT connection ===
  
  // === Start click by user ===
  $('#publish').click(function(event) {
    var topic = $('#topic').val();
    var message = $('#message').val()
    if(message==="remove"){
      message = message+' '+$('#optionMessage').val()+" "+$('#object').val();
    }
    else{
      message = message+' '+$('#optionMessage').val();
    }

    var data = '{"topic": "' + topic + '", "message": "' + message + '"}';
    socket.emit('publish', data=data);
  });

  $('#subscribe').click(function(event) {
    var topic = $('#subscribe_topic').val();
    var data = '{"topic": "' + topic + '"}';
    socket.emit('subscribe', data=data);
    $('#subscribe').hide();
    $('#unsubscribe').show();
    $('#subscribe_topic').prop('readonly', true);
    $('#subscribe_messages').val('');
    $('#pubDevice').attr("disabled","disabled"); 
  });

  $('#unsubscribe').click(function(event) {
    var data = $('#subscribe_topic').val();
    socket.emit('unsubscribe_all',data=data);
    $('#subscribe').show();
    $('#unsubscribe').hide();
    $('#pubDevice').removeAttr('disabled'); 
  });

  // register a device
  $('#register').click(function(event) {
    var name = $('#regQueue option:selected');
    var hostname = $('#hostname');
    var osname = $('#osname');
    var cpus = $('#cpus');
    var ipAddr = $('#ipAddr');
    
    getList("devices",httpRequest1);
    var id = $('#deviceNum').val();
    var data = '{"id": "' + id + '", "ipv4Addr": "' + ipAddr.val() + '", "name": "'+ name.val()
    + '", "hostname": "'+ hostname.val()+ '", "cpu_count": "'+ cpus.val() 
    + '", "os_system": "'+ osname.val()+ '"}';
    getList("removeQueue/"+name.val(),httpRequest3);
    socket.emit('register', data=data);
    
    name.val('');
    hostname.val('');
    osname.val('');
    cpus.val('');
    ipAddr.val('');

  });
  // === End click by user ===

  // === Address the mqtt message ===
  socket.on('mqtt_message', function(data) {
    var topic = data['topic'];
    var sub_topic = $('#subscribe_topic').val();

    // 1. receive message for checking connection 
    if(topic==="RST"){
      var name = data['payload']
      console.log(name);
      a = devicesNameList_copy.length
      devicesNameList_copy = devicesNameList_copy.filter(e => e !== name);
      if(a!=devicesNameList_copy.length){
        changeConn(name,"True");
      }
      console.log("After:",devicesNameList_copy);
    }

    // 2. receive the result of command
    else if(sub_topic == topic){
      var text = data['payload'];
      var $textarea = $('#subscribe_messages');

      if(text == "\n"){
        text = "The command line has a problem. \n"
      }
      else{
        text=text.replace(/minutes/gi,"m");
        text=text.replace(/hours/gi,"h");
        text=text.replace(/seconds/gi,"s");
        text=text.replace(/        /gi,"    ");
      }
      $textarea.val($textarea.val() + "=========  The Result =========" + '\n');
      $textarea.val($textarea.val() + text + '\n');
    }
  });
  // === End mqtt message ===

  function changeSelect(){
    var topic = $('#topic');
    var sub_topic = $('#subscribe_topic');
    var selectVal = $('#pubDevice option:selected').val();
    topic.val(selectVal);
    var sub = (selectVal=='')? '':selectVal+"_result";
    sub_topic.val(sub);
  }

  // === Start change by user ===
  $('#pubDevice').change(changeSelect);
  
  $('#regQueue').change(function(){
    var selectVal = $('#regQueue option:selected').val();
    getList("registerQueue/"+selectVal,httpRequest3);
  });
  
  $('#message').change(function(){
    $('#optionMessage').val('');
    var option = $('#message').val();
    if(option==='remove'){
      $('#object').removeAttr('disabled'); 
    }
    else{
      $('#object').attr("disabled","disabled"); 
    }
  });
  // === End change by user ===
    
  // === Start httpRequest ===
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
              var url = httpRequest.responseURL;
              console.log(url);
              printListDetail(url,httpRequest);
            }
        }
    }
    catch(e){
      console.log(e.message);
    }
  }
    
  function printListDetail(url,httpRequest){

    // 1. Start to get the list of all devices
    if(url.endsWith("devices")){
      var list = JSON.parse(httpRequest.responseText);
      var deviceList = $('#pubDevice');
      var deviceTable=$('#deviceTable');
      var selectVal = $('#pubDevice option:selected').val();
      console.log("sv >:",selectVal);

      deviceList.empty();
      deviceTable.empty();

      var headline = '<div class="row2 header"><div class="cell">No.</div>'+
      '<div class="cell">DEVICE NAME</div><div class="cell">IP ADDRESS</div><div class="cell">CPU</div>'+
      '<div class="cell">REGISTER DATE</div><div class="cell">HOSTNAME</div><div class="cell">OS</div>'+
      '<div class="cell">CONNECTED</div></div>';
      deviceTable.append(headline);

      if(selectVal==undefined || selectVal==''){
        deviceList.append("<option value='' selected disabled >Select a device</option>");
      }
      else{
        deviceList.append("<option value='' disabled >Select a device</option>");
      }
      
      devicesNameList=[];
      
      for(var count = 0; count < list.length; ++count){
        if(!list[count]["connected"]){
          deviceList.append("<option value='"+list[count]["name"]+"' disabled>"
          +list[count]["name"]+" (disconnected)"+"</option>");
          if(list[count]["name"]==selectVal){
            // turn to 'Select a device'
            deviceList.find("option:eq(0)").prop("selected", true);
            alert("The selected device is disconnected.")
          }
        }
        else{
          if(list[count]["name"]==selectVal){
            deviceList.append("<option value='"+list[count]["name"]+"' selected>"
            +list[count]["name"]+"</option>");
          }else{
            deviceList.append("<option value='"+list[count]["name"]+"'>"
            +list[count]["name"]+"</option>");
          }
          
        }
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
    // End all devices

    // 2. get the list of all waiting devices
    else if(url.endsWith("registerQueue")){
      var list = JSON.parse(httpRequest.responseText);
      var deviceList = $('#regQueue');
      var selectVal = $('#regQueue option:selected').val();
      deviceList.empty();
      if(selectVal==undefined || selectVal==''){
        deviceList.append("<option value='' selected disabled >Select a device</option>");
      }
      else{
        deviceList.append("<option value='' disabled >Select a device</option>");
      }
      
      for(var count = 0; count < list.length; ++count){
        if(list[count]["name"]==selectVal){
          deviceList.append("<option value='"+list[count]["name"]+"' selected>"
        +list[count]["name"]+"</option>");
        }
        else{
          deviceList.append("<option value='"+list[count]["name"]+"'>"
          +list[count]["name"]+"</option>");
        }
      }
    }
    // End all waiting devices
    
    // 3. get the info of a selected waiting device
    else if(url.indexOf("/registerQueue/")>0){
      var list = JSON.parse(httpRequest.responseText);
      $('#hostname').val(list["hostname"]);
      $('#osname').val(list["os_system"]);
      $('#cpus').val(list["cpu_count"]);
      $('#ipAddr').val(list["ipv4Addr"]);
    }
    // 4. after remove a waiting device
    else if(url.indexOf("/removeQueue/")>0){
      getList("registerQueue",httpRequest2);
      getList("devices",httpRequest1);
    }
  }

  // Start to change the connection status
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


});


  