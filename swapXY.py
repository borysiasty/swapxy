# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#
# Swap XY
# Copyright (C) 2010-2013 Borys Jurgiel
#
#----------------------------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#----------------------------------------------------------------------------

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.utils import plugins

import resources_rc


class SwapXY:


    def __init__(self, iface):
        self.iface = iface


    def initGui(self):
        self.action = QAction(QIcon(':/plugins/swapXY/swapXYIcon.png'), 'Swap XY', self.iface.mainWindow())
        self.action.setWhatsThis('Swaps coordinate order')
        QObject.connect(self.action, SIGNAL('triggered()'), self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu('Swap XY', self.action)


    def unload(self):
        self.iface.removePluginMenu('Swap XY',self.action)
        self.iface.removeToolBarIcon(self.action)


    def run(self):
        layer = self.iface.mapCanvas().currentLayer()
        if not layer:
            QMessageBox.warning(self.iface.mainWindow(), 'Swap XY', 'No layer selected')
            return
        if layer.type() != layer.VectorLayer: # or layer.geometryType() != QGis.Point:
            QMessageBox.warning(self.iface.mainWindow(), 'Swap XY', 'Only vector layers are supported')
            return

        if not layer.dataProvider().capabilities() & QgsVectorDataProvider.ChangeGeometries:
            QMessageBox.warning(self.iface.mainWindow(), 'Swap XY', 'This data format doesn\'t allow to modify geometries. Please convert to another format first.')
            return

        msg = u'Are you sure you want to swap order of coordinates on the following layer?<br/><br/><b>%s</b><br/><br/>' % layer.name()
        msg += 'Please read important notes below:<br/><br/>'

        msg += 'In case of failure when processing one or more features, this tool may damage your data. Always make sure you have a backup.<br/><br/>'
        msg += 'If the data has been partially swapped, you can run this tool again to revert the swap. You can also run it with a feature selection in order to only process invalid features.<br/><br/>'
        msg += 'The new data extents declaration may be not written permanently to the file. In this case zooming to layer extent will be broken once you load the swapped layer again. In this case please save data to a new layer.<br/><br/>'
        msg += 'This process may take a long time, depending on the number of vertices to swap.'

        if QMessageBox.question(self.iface.mainWindow(), 'Swap XY', msg, QMessageBox.Yes, QMessageBox.No) == QMessageBox.No:
            return

        if layer.selectedFeatures() and QMessageBox.question(self.iface.mainWindow(), 'Swap XY', u'<b>WARNING!</b> Some features on the layer are selected. Are you really sure you want to only process selected features? This is normally only usable to fix partially converted layer. If you want to process all features, please choose "No".', QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
            processSelectedFeaturesOnly = True
        else:
            processSelectedFeaturesOnly = False

        QApplication.setOverrideCursor(Qt.WaitCursor)

        layer.startEditing()

        if processSelectedFeaturesOnly:
            # call invertSelection twice, as you have to touch the layer selection after calling startEditing (!)
            layer.invertSelection()
        else:
            # select all features by calling removeSelection and then invertSelection
            layer.removeSelection()

        layer.invertSelection()

        if QGis.QGIS_VERSION_INT < 20000:
            # QGIS API v1
            feat = QgsFeature()
            for fid in layer.selectedFeaturesIds():
                layer.featureAtId(fid,feat)
                geom=feat.geometry()
                i=0
                vertex=geom.vertexAt(i)
                while (vertex!=QgsPoint(0,0)):
                    x=vertex.x()
                    y=vertex.y()
                    layer.moveVertex(y,x,fid,i)
                    i+=1
                    vertex=geom.vertexAt(i)
        else:
            # QGIS API v2
            layer.beginEditCommand('swapXY')
            for feat in layer.selectedFeatures():
                fid = feat.id()
                geom=feat.geometry()
                i=0
                vertex=geom.vertexAt(i)
                while (vertex!=QgsPoint(0,0)):
                    x=vertex.x()
                    y=vertex.y()
                    layer.moveVertex(y,x,fid,i)
                    i+=1
                    vertex=geom.vertexAt(i)
            layer.endEditCommand()

        layer.updateExtents()
        layer.commitChanges()
        layer.updateExtents()
        self.iface.mapCanvas().refresh()
        if processSelectedFeaturesOnly:
            layer.removeSelection()
            layer.invertSelection()
        self.iface.mapCanvas().zoomToSelected()
        layer.removeSelection()

        QApplication.restoreOverrideCursor()
