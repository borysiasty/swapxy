# -*- coding: utf-8 -*-
########################################################
#                                         __init__.py  #
########################################################
#    SwapXY plugin
#    Copyright (C) 2010-2013 Borys Jurgiel
#    email: qgis@borysjurgiel.pl
########################################################
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of the GNU General Public License is available at
#    http://www.gnu.org/licenses/gpl.txt, or can be requested to the Free
#    Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#    Boston, MA 02110-1301 USA.
#
########################################################

def name():
  return 'Swap XY'

def description():
  return 'Swaps coordinate order of vector layer (X,Y -> Y,X)'

def version():
  return 'Version 0.1.2'

def qgisMinimumVersion():
  return '1.6'

def qgisMaximumVersion():
  return '2.99'

def authorName():
  return 'Borys Jurgiel'

def author():
  return authorName()

def email():
  return 'qgis at borysjurgiel dot pl'

def homepage():
  return 'www.borysjurgiel.pl'

def experimental():
  return True

def classFactory(iface):
  from swapXY import SwapXY
  return SwapXY(iface)
