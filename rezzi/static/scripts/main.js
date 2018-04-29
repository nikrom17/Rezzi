var myApp = angular.module('helloworld', ['ui.router']);

myApp.config(function($stateProvider) {
  var homeState = {
    name: 'home',
    url: '/home',
    templateUrl: './templates/home.html'
  }
  
  var resumeState = {
    name: 'resume',
    url: '/resume',
    templateUrl: './templates/resume.html'
  }
  
  var chatState = {
    name: 'chat',
    url: '/chat',
    templateUrl: './templates/chat.html'
  }

  $stateProvider.state(homeState);
  $stateProvider.state(resumeState);
  $stateProvider.state(chatState);
});