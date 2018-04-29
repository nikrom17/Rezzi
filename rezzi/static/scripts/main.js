var myApp = angular.module('helloworld', ['ui.router']);

myApp.controller('chatCtrl', ['$http','$scope',function($http,$scope) {

    // get data from flask
    $scope.socket = null;

    $scope.record = function($event){
      $event.preventDefault();
      /*console.log("recording...");
      if($scope.socket == null){
        $scope.socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
        $scope.socket.on('connect', function() {
            navigator.getUserMedia({audio: true}, initializeRecorder, function(a, b, c){
              console.log(a, b, c);
            });
        });
      }
      else {
        $scope.socket.disconnect();
        $scope.socket.connect();
      }*/
      $event.currentTarget.querySelector("button").disabled = true;
      /*$('#connect input')[0].disabled = true;
      $('#disconnect input')[0].disabled = false;*/
    }

    $scope.stopRecord = function($event){
      $event.preventDefault();
      $event.currentTarget.querySelector("button").disabled = false;
    }
}]);

myApp.config(function($stateProvider, $urlRouterProvider) {

  $urlRouterProvider.otherwise("/home");
  var homeState = {
    name: 'home',
    url: '/home',
    templateUrl: './views/home.html'
  }
  
  var resumeState = {
    name: 'resume',
    url: '/resume',
    templateUrl: './views/resume.html'
  }
  
  var chatState = {
    name: 'chat',
    url: '/chat',
    templateUrl: './views/chat.html'
  }

  $stateProvider
    .state(homeState)
    .state(resumeState)
    .state(chatState);
});

 // audio functions
function initializeRecorder(stream){
   mediaStream = stream;

   // get sample rate
   audio_context = new AudioContext;
   sampleRate = audio_context.sampleRate;
   console.log('<sample_rate>', sampleRate);
   socket.emit('sample_rate', sampleRate);

   var audioInput = audio_context.createMediaStreamSource(stream);

   console.log("Created media stream.");

   var bufferSize = 4096;
   // record only 1 channel
   var recorder = audio_context.createScriptProcessor(bufferSize, 1, 1);
   // specify the processing function
   recorder.onaudioprocess = recorderProcess;
   // connect stream to our recorder
   audioInput.connect(recorder);
   // connect our recorder to the previous destination
   recorder.connect(audio_context.destination);          
}
function recorderProcess(e) {
  var left = e.inputBuffer.getChannelData(0);
  socket.emit('audio', left);
}
function convertFloat32ToInt16(buffer) {
  l = buffer.length;
  buf = new Int16Array(l);
  while (l--) {
    buf[l] = Math.min(1, buffer[l])*0x7FFF;
  }
  console.log(buf);
  return buf.buffer;
}