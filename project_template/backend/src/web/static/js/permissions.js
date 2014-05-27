var app = angular.module('app', ['rest'])
    .controller('AppCtrl', ['$scope', 'RestApi', function ($scope, RestApi) {
        $scope.users = [];
        $scope.searchingUsersFlag = false;
        $scope.moreResultsFlag = false;
        $scope.searchPrefix = ''
        $scope.searchUsers = function (emailPrefix) {
            $scope.searchPrefix = emailPrefix;
            $scope.searchingUsersFlag = true;
            RestApi.searchUsers(emailPrefix).success(function (obj) {
                $scope.users = obj.users;
                $scope.moreResultsFlag = obj.more;
                $scope.nextPage = obj.next_page;
            }).always(function () {
                $scope.searchingUsersFlag = false;
            });
        }
        $scope.searchUsers('');
    }]);

app.directive('permform', function () {
    return{
        restrict: 'E',
        replace: true,
        templateUrl: '/static/html/permission_form.html',
        scope: {
            search: '=',
            showButton: '='
        },
        controller: ['$scope', function ($scope) {
            $scope.emailPrefix = '';
        }]
    };
});

app.directive('permtable', function () {
    return{
        restrict: 'E',
        replace: true,
        templateUrl: '/static/html/permission_table.html',
        scope: {
            users: '=',
            nextPage: '=',
            showTable: '=',
            moreResultsFlag: '=',
            searchPrefix: '='
        },
        controller: ['$scope', 'RestApi', function ($scope, rest) {
            $scope.searchingNextPage = false;


            $scope.searchNextPage = function (nextPage) {
                $scope.searchingNextPage = true;
                rest.searchNextPage(nextPage).success(function (obj) {
                    for (var i = 0; i < obj.users.length; i++) {
                        $scope.users.push(obj.users[i]);
                    }
                    $scope.nextPage = obj.next_page;
                    $scope.moreResultsFlag = obj.more;
                }).always(function () {
                    $scope.searchingNextPage = false;
                });
            }
        }]
    };
});