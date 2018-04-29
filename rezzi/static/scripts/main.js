var myApp = angular.module('helloworld', ['ui.router']);

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