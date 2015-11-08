__author__ = 'Jiaxiang'

from rest_framework import permissions


class AllowOperator(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            if request.user.concreteuser.type == "operator":
                return True
            else:
                return False
        except Exception as e:
            print(e.__str__())
            return False

class AllowKeyDecisionMaker(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            if request.user.concreteuser.type == "kdm":
                return True
            else:
                return False
        except Exception as e:
            print(e.__str__())
            return False

class AllowCrisisManager(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            if request.user.concreteuser.type == "crisis_manager":
                return True
            else:
                return False
        except Exception as e:
            print(e.__str__())
            return False

class AllowManagerAndKdm(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            type = request.user.concreteuser.type
            if  type=="crisis_manager" or type=="kdm":
                return True
            else:
                return False
        except Exception as e:
            print(e.__str__())
            return False


class AllowOperatorAndManager(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            type = request.user.concreteuser.type
            if  type=="crisis_manager" or type=="operator":
                return True
            else:
                return False
        except Exception as e:
            print(e.__str__())
            return False


class AllowThreeTypes(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            type = request.user.concreteuser.type
            if  type=="crisis_manager" or type=="operator" or type=="kdm":
                return True
            else:
                return False
        except Exception as e:
            print(e.__str__())
            return False