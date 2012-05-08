###############################################################################
##
## Copyright (C) 2006-2011, University of Utah. 
## All rights reserved.
## Contact: contact@vistrails.org
##
## This file is part of VisTrails.
##
## "Redistribution and use in source and binary forms, with or without 
## modification, are permitted provided that the following conditions are met:
##
##  - Redistributions of source code must retain the above copyright notice, 
##    this list of conditions and the following disclaimer.
##  - Redistributions in binary form must reproduce the above copyright 
##    notice, this list of conditions and the following disclaimer in the 
##    documentation and/or other materials provided with the distribution.
##  - Neither the name of the University of Utah nor the names of its 
##    contributors may be used to endorse or promote products derived from 
##    this software without specific prior written permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
## AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
## THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
## PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
## CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
## EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
## PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; 
## OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
## WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
## OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
## ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
###############################################################################

"""generated automatically by auto_dao.py"""

import copy

class DBConnection(object):

    vtType = 'connection'

    def __init__(self, id=None, ports=None):
        self._db_id = id
        self.db_deleted_ports = []
        self.db_ports_id_index = {}
        self.db_ports_type_index = {}
        if ports is None:
            self._db_ports = []
        else:
            self._db_ports = ports
            for v in self._db_ports:
                self.db_ports_id_index[v.db_id] = v
                self.db_ports_type_index[v.db_type] = v
        self.is_dirty = True
        self.is_new = True
    
    def __copy__(self):
        return DBConnection.do_copy(self)

    def do_copy(self, new_ids=False, id_scope=None, id_remap=None):
        cp = DBConnection(id=self._db_id)
        if self._db_ports is None:
            cp._db_ports = []
        else:
            cp._db_ports = [v.do_copy(new_ids, id_scope, id_remap) for v in self._db_ports]
        
        # set new ids
        if new_ids:
            new_id = id_scope.getNewId(self.vtType)
            if self.vtType in id_scope.remap:
                id_remap[(id_scope.remap[self.vtType], self.db_id)] = new_id
            else:
                id_remap[(self.vtType, self.db_id)] = new_id
            cp.db_id = new_id
        
        # recreate indices and set flags
        cp.db_ports_id_index = dict((v.db_id, v) for v in cp._db_ports)
        cp.db_ports_type_index = dict((v.db_type, v) for v in cp._db_ports)
        if not new_ids:
            cp.is_dirty = self.is_dirty
            cp.is_new = self.is_new
        return cp

    @staticmethod
    def update_version(old_obj, trans_dict, new_obj=None):
        if new_obj is None:
            new_obj = DBConnection()
        class_dict = {}
        if new_obj.__class__.__name__ in trans_dict:
            class_dict = trans_dict[new_obj.__class__.__name__]
        if 'id' in class_dict:
            res = class_dict['id'](old_obj, trans_dict)
            new_obj.db_id = res
        elif hasattr(old_obj, 'db_id') and old_obj.db_id is not None:
            new_obj.db_id = old_obj.db_id
        if 'ports' in class_dict:
            res = class_dict['ports'](old_obj, trans_dict)
            for obj in res:
                new_obj.db_add_port(obj)
        elif hasattr(old_obj, 'db_ports') and old_obj.db_ports is not None:
            for obj in old_obj.db_ports:
                new_obj.db_add_port(DBPort.update_version(obj, trans_dict))
        if hasattr(old_obj, 'db_deleted_ports') and hasattr(new_obj, 'db_deleted_ports'):
            for obj in old_obj.db_deleted_ports:
                n_obj = DBPort.update_version(obj, trans_dict)
                new_obj.db_deleted_ports.append(n_obj)
        new_obj.is_new = old_obj.is_new
        new_obj.is_dirty = old_obj.is_dirty
        return new_obj

    def db_children(self, parent=(None,None), orphan=False):
        children = []
        to_del = []
        for child in self.db_ports:
            children.extend(child.db_children((self.vtType, self.db_id), orphan))
            if orphan:
                to_del.append(child)
        for child in to_del:
            self.db_delete_port(child)
        children.append((self, parent[0], parent[1]))
        return children
    def db_deleted_children(self, remove=False):
        children = []
        children.extend(self.db_deleted_ports)
        if remove:
            self.db_deleted_ports = []
        return children
    def has_changes(self):
        if self.is_dirty:
            return True
        for child in self._db_ports:
            if child.has_changes():
                return True
        return False
    def __get_db_id(self):
        return self._db_id
    def __set_db_id(self, id):
        self._db_id = id
        self.is_dirty = True
    db_id = property(__get_db_id, __set_db_id)
    def db_add_id(self, id):
        self._db_id = id
    def db_change_id(self, id):
        self._db_id = id
    def db_delete_id(self, id):
        self._db_id = None
    
    def __get_db_ports(self):
        return self._db_ports
    def __set_db_ports(self, ports):
        self._db_ports = ports
        self.is_dirty = True
    db_ports = property(__get_db_ports, __set_db_ports)
    def db_get_ports(self):
        return self._db_ports
    def db_add_port(self, port):
        self.is_dirty = True
        self._db_ports.append(port)
        self.db_ports_id_index[port.db_id] = port
        self.db_ports_type_index[port.db_type] = port
    def db_change_port(self, port):
        self.is_dirty = True
        found = False
        for i in xrange(len(self._db_ports)):
            if self._db_ports[i].db_id == port.db_id:
                self._db_ports[i] = port
                found = True
                break
        if not found:
            self._db_ports.append(port)
        self.db_ports_id_index[port.db_id] = port
        self.db_ports_type_index[port.db_type] = port
    def db_delete_port(self, port):
        self.is_dirty = True
        for i in xrange(len(self._db_ports)):
            if self._db_ports[i].db_id == port.db_id:
                if not self._db_ports[i].is_new:
                    self.db_deleted_ports.append(self._db_ports[i])
                del self._db_ports[i]
                break
        del self.db_ports_id_index[port.db_id]
        del self.db_ports_type_index[port.db_type]
    def db_get_port(self, key):
        for i in xrange(len(self._db_ports)):
            if self._db_ports[i].db_id == key:
                return self._db_ports[i]
        return None
    def db_get_port_by_id(self, key):
        return self.db_ports_id_index[key]
    def db_has_port_with_id(self, key):
        return key in self.db_ports_id_index
    def db_get_port_by_type(self, key):
        return self.db_ports_type_index[key]
    def db_has_port_with_type(self, key):
        return key in self.db_ports_type_index
    
    def getPrimaryKey(self):
        return self._db_id

class DBPortSpec(object):

    vtType = 'portSpec'

    def __init__(self, id=None, name=None, type=None, optional=None, sort_key=None, sigstring=None):
        self._db_id = id
        self._db_name = name
        self._db_type = type
        self._db_optional = optional
        self._db_sort_key = sort_key
        self._db_sigstring = sigstring
        self.is_dirty = True
        self.is_new = True
    
    def __copy__(self):
        return DBPortSpec.do_copy(self)

    def do_copy(self, new_ids=False, id_scope=None, id_remap=None):
        cp = DBPortSpec(id=self._db_id,
                        name=self._db_name,
                        type=self._db_type,
                        optional=self._db_optional,
                        sort_key=self._db_sort_key,
                        sigstring=self._db_sigstring)
        
        # set new ids
        if new_ids:
            new_id = id_scope.getNewId(self.vtType)
            if self.vtType in id_scope.remap:
                id_remap[(id_scope.remap[self.vtType], self.db_id)] = new_id
            else:
                id_remap[(self.vtType, self.db_id)] = new_id
            cp.db_id = new_id
        
        # recreate indices and set flags
        if not new_ids:
            cp.is_dirty = self.is_dirty
            cp.is_new = self.is_new
        return cp

    @staticmethod
    def update_version(old_obj, trans_dict, new_obj=None):
        if new_obj is None:
            new_obj = DBPortSpec()
        class_dict = {}
        if new_obj.__class__.__name__ in trans_dict:
            class_dict = trans_dict[new_obj.__class__.__name__]
        if 'id' in class_dict:
            res = class_dict['id'](old_obj, trans_dict)
            new_obj.db_id = res
        elif hasattr(old_obj, 'db_id') and old_obj.db_id is not None:
            new_obj.db_id = old_obj.db_id
        if 'name' in class_dict:
            res = class_dict['name'](old_obj, trans_dict)
            new_obj.db_name = res
        elif hasattr(old_obj, 'db_name') and old_obj.db_name is not None:
            new_obj.db_name = old_obj.db_name
        if 'type' in class_dict:
            res = class_dict['type'](old_obj, trans_dict)
            new_obj.db_type = res
        elif hasattr(old_obj, 'db_type') and old_obj.db_type is not None:
            new_obj.db_type = old_obj.db_type
        if 'optional' in class_dict:
            res = class_dict['optional'](old_obj, trans_dict)
            new_obj.db_optional = res
        elif hasattr(old_obj, 'db_optional') and old_obj.db_optional is not None:
            new_obj.db_optional = old_obj.db_optional
        if 'sort_key' in class_dict:
            res = class_dict['sort_key'](old_obj, trans_dict)
            new_obj.db_sort_key = res
        elif hasattr(old_obj, 'db_sort_key') and old_obj.db_sort_key is not None:
            new_obj.db_sort_key = old_obj.db_sort_key
        if 'sigstring' in class_dict:
            res = class_dict['sigstring'](old_obj, trans_dict)
            new_obj.db_sigstring = res
        elif hasattr(old_obj, 'db_sigstring') and old_obj.db_sigstring is not None:
            new_obj.db_sigstring = old_obj.db_sigstring
        new_obj.is_new = old_obj.is_new
        new_obj.is_dirty = old_obj.is_dirty
        return new_obj

    def db_children(self, parent=(None,None), orphan=False):
        return [(self, parent[0], parent[1])]
    def db_deleted_children(self, remove=False):
        children = []
        return children
    def has_changes(self):
        if self.is_dirty:
            return True
        return False
    def __get_db_id(self):
        return self._db_id
    def __set_db_id(self, id):
        self._db_id = id
        self.is_dirty = True
    db_id = property(__get_db_id, __set_db_id)
    def db_add_id(self, id):
        self._db_id = id
    def db_change_id(self, id):
        self._db_id = id
    def db_delete_id(self, id):
        self._db_id = None
    
    def __get_db_name(self):
        return self._db_name
    def __set_db_name(self, name):
        self._db_name = name
        self.is_dirty = True
    db_name = property(__get_db_name, __set_db_name)
    def db_add_name(self, name):
        self._db_name = name
    def db_change_name(self, name):
        self._db_name = name
    def db_delete_name(self, name):
        self._db_name = None
    
    def __get_db_type(self):
        return self._db_type
    def __set_db_type(self, type):
        self._db_type = type
        self.is_dirty = True
    db_type = property(__get_db_type, __set_db_type)
    def db_add_type(self, type):
        self._db_type = type
    def db_change_type(self, type):
        self._db_type = type
    def db_delete_type(self, type):
        self._db_type = None
    
    def __get_db_optional(self):
        return self._db_optional
    def __set_db_optional(self, optional):
        self._db_optional = optional
        self.is_dirty = True
    db_optional = property(__get_db_optional, __set_db_optional)
    def db_add_optional(self, optional):
        self._db_optional = optional
    def db_change_optional(self, optional):
        self._db_optional = optional
    def db_delete_optional(self, optional):
        self._db_optional = None
    
    def __get_db_sort_key(self):
        return self._db_sort_key
    def __set_db_sort_key(self, sort_key):
        self._db_sort_key = sort_key
        self.is_dirty = True
    db_sort_key = property(__get_db_sort_key, __set_db_sort_key)
    def db_add_sort_key(self, sort_key):
        self._db_sort_key = sort_key
    def db_change_sort_key(self, sort_key):
        self._db_sort_key = sort_key
    def db_delete_sort_key(self, sort_key):
        self._db_sort_key = None
    
    def __get_db_sigstring(self):
        return self._db_sigstring
    def __set_db_sigstring(self, sigstring):
        self._db_sigstring = sigstring
        self.is_dirty = True
    db_sigstring = property(__get_db_sigstring, __set_db_sigstring)
    def db_add_sigstring(self, sigstring):
        self._db_sigstring = sigstring
    def db_change_sigstring(self, sigstring):
        self._db_sigstring = sigstring
    def db_delete_sigstring(self, sigstring):
        self._db_sigstring = None
    
    def getPrimaryKey(self):
        return self._db_id

class DBModuleDescriptor(object):

    vtType = 'module_descriptor'

    def __init__(self, id=None, name=None, package=None, namespace=None, version=None, base_descriptor_id=None, portSpecs=None):
        self._db_id = id
        self._db_name = name
        self._db_package = package
        self._db_namespace = namespace
        self._db_version = version
        self._db_base_descriptor_id = base_descriptor_id
        self.db_deleted_portSpecs = []
        self.db_portSpecs_id_index = {}
        self.db_portSpecs_name_index = {}
        if portSpecs is None:
            self._db_portSpecs = []
        else:
            self._db_portSpecs = portSpecs
            for v in self._db_portSpecs:
                self.db_portSpecs_id_index[v.db_id] = v
                self.db_portSpecs_name_index[(v.db_name,v.db_type)] = v
        self.is_dirty = True
        self.is_new = True
    
    def __copy__(self):
        return DBModuleDescriptor.do_copy(self)

    def do_copy(self, new_ids=False, id_scope=None, id_remap=None):
        cp = DBModuleDescriptor(id=self._db_id,
                                name=self._db_name,
                                package=self._db_package,
                                namespace=self._db_namespace,
                                version=self._db_version,
                                base_descriptor_id=self._db_base_descriptor_id)
        if self._db_portSpecs is None:
            cp._db_portSpecs = []
        else:
            cp._db_portSpecs = [v.do_copy(new_ids, id_scope, id_remap) for v in self._db_portSpecs]
        
        # set new ids
        if new_ids:
            new_id = id_scope.getNewId(self.vtType)
            if self.vtType in id_scope.remap:
                id_remap[(id_scope.remap[self.vtType], self.db_id)] = new_id
            else:
                id_remap[(self.vtType, self.db_id)] = new_id
            cp.db_id = new_id
            if hasattr(self, 'db_base_descriptor_id') and ('module_descriptor', self._db_base_descriptor_id) in id_remap:
                cp._db_base_descriptor_id = id_remap[('module_descriptor', self._db_base_descriptor_id)]
        
        # recreate indices and set flags
        cp.db_portSpecs_id_index = dict((v.db_id, v) for v in cp._db_portSpecs)
        cp.db_portSpecs_name_index = dict(((v.db_name,v.db_type), v) for v in cp._db_portSpecs)
        if not new_ids:
            cp.is_dirty = self.is_dirty
            cp.is_new = self.is_new
        return cp

    @staticmethod
    def update_version(old_obj, trans_dict, new_obj=None):
        if new_obj is None:
            new_obj = DBModuleDescriptor()
        class_dict = {}
        if new_obj.__class__.__name__ in trans_dict:
            class_dict = trans_dict[new_obj.__class__.__name__]
        if 'id' in class_dict:
            res = class_dict['id'](old_obj, trans_dict)
            new_obj.db_id = res
        elif hasattr(old_obj, 'db_id') and old_obj.db_id is not None:
            new_obj.db_id = old_obj.db_id
        if 'name' in class_dict:
            res = class_dict['name'](old_obj, trans_dict)
            new_obj.db_name = res
        elif hasattr(old_obj, 'db_name') and old_obj.db_name is not None:
            new_obj.db_name = old_obj.db_name
        if 'package' in class_dict:
            res = class_dict['package'](old_obj, trans_dict)
            new_obj.db_package = res
        elif hasattr(old_obj, 'db_package') and old_obj.db_package is not None:
            new_obj.db_package = old_obj.db_package
        if 'namespace' in class_dict:
            res = class_dict['namespace'](old_obj, trans_dict)
            new_obj.db_namespace = res
        elif hasattr(old_obj, 'db_namespace') and old_obj.db_namespace is not None:
            new_obj.db_namespace = old_obj.db_namespace
        if 'version' in class_dict:
            res = class_dict['version'](old_obj, trans_dict)
            new_obj.db_version = res
        elif hasattr(old_obj, 'db_version') and old_obj.db_version is not None:
            new_obj.db_version = old_obj.db_version
        if 'base_descriptor_id' in class_dict:
            res = class_dict['base_descriptor_id'](old_obj, trans_dict)
            new_obj.db_base_descriptor_id = res
        elif hasattr(old_obj, 'db_base_descriptor_id') and old_obj.db_base_descriptor_id is not None:
            new_obj.db_base_descriptor_id = old_obj.db_base_descriptor_id
        if 'portSpecs' in class_dict:
            res = class_dict['portSpecs'](old_obj, trans_dict)
            for obj in res:
                new_obj.db_add_portSpec(obj)
        elif hasattr(old_obj, 'db_portSpecs') and old_obj.db_portSpecs is not None:
            for obj in old_obj.db_portSpecs:
                new_obj.db_add_portSpec(DBPortSpec.update_version(obj, trans_dict))
        if hasattr(old_obj, 'db_deleted_portSpecs') and hasattr(new_obj, 'db_deleted_portSpecs'):
            for obj in old_obj.db_deleted_portSpecs:
                n_obj = DBPortSpec.update_version(obj, trans_dict)
                new_obj.db_deleted_portSpecs.append(n_obj)
        new_obj.is_new = old_obj.is_new
        new_obj.is_dirty = old_obj.is_dirty
        return new_obj

    def db_children(self, parent=(None,None), orphan=False):
        children = []
        to_del = []
        for child in self.db_portSpecs:
            children.extend(child.db_children((self.vtType, self.db_id), orphan))
            if orphan:
                to_del.append(child)
        for child in to_del:
            self.db_delete_portSpec(child)
        children.append((self, parent[0], parent[1]))
        return children
    def db_deleted_children(self, remove=False):
        children = []
        children.extend(self.db_deleted_portSpecs)
        if remove:
            self.db_deleted_portSpecs = []
        return children
    def has_changes(self):
        if self.is_dirty:
            return True
        for child in self._db_portSpecs:
            if child.has_changes():
                return True
        return False
    def __get_db_id(self):
        return self._db_id
    def __set_db_id(self, id):
        self._db_id = id
        self.is_dirty = True
    db_id = property(__get_db_id, __set_db_id)
    def db_add_id(self, id):
        self._db_id = id
    def db_change_id(self, id):
        self._db_id = id
    def db_delete_id(self, id):
        self._db_id = None
    
    def __get_db_name(self):
        return self._db_name
    def __set_db_name(self, name):
        self._db_name = name
        self.is_dirty = True
    db_name = property(__get_db_name, __set_db_name)
    def db_add_name(self, name):
        self._db_name = name
    def db_change_name(self, name):
        self._db_name = name
    def db_delete_name(self, name):
        self._db_name = None
    
    def __get_db_package(self):
        return self._db_package
    def __set_db_package(self, package):
        self._db_package = package
        self.is_dirty = True
    db_package = property(__get_db_package, __set_db_package)
    def db_add_package(self, package):
        self._db_package = package
    def db_change_package(self, package):
        self._db_package = package
    def db_delete_package(self, package):
        self._db_package = None
    
    def __get_db_namespace(self):
        return self._db_namespace
    def __set_db_namespace(self, namespace):
        self._db_namespace = namespace
        self.is_dirty = True
    db_namespace = property(__get_db_namespace, __set_db_namespace)
    def db_add_namespace(self, namespace):
        self._db_namespace = namespace
    def db_change_namespace(self, namespace):
        self._db_namespace = namespace
    def db_delete_namespace(self, namespace):
        self._db_namespace = None
    
    def __get_db_version(self):
        return self._db_version
    def __set_db_version(self, version):
        self._db_version = version
        self.is_dirty = True
    db_version = property(__get_db_version, __set_db_version)
    def db_add_version(self, version):
        self._db_version = version
    def db_change_version(self, version):
        self._db_version = version
    def db_delete_version(self, version):
        self._db_version = None
    
    def __get_db_base_descriptor_id(self):
        return self._db_base_descriptor_id
    def __set_db_base_descriptor_id(self, base_descriptor_id):
        self._db_base_descriptor_id = base_descriptor_id
        self.is_dirty = True
    db_base_descriptor_id = property(__get_db_base_descriptor_id, __set_db_base_descriptor_id)
    def db_add_base_descriptor_id(self, base_descriptor_id):
        self._db_base_descriptor_id = base_descriptor_id
    def db_change_base_descriptor_id(self, base_descriptor_id):
        self._db_base_descriptor_id = base_descriptor_id
    def db_delete_base_descriptor_id(self, base_descriptor_id):
        self._db_base_descriptor_id = None
    
    def __get_db_portSpecs(self):
        return self._db_portSpecs
    def __set_db_portSpecs(self, portSpecs):
        self._db_portSpecs = portSpecs
        self.is_dirty = True
    db_portSpecs = property(__get_db_portSpecs, __set_db_portSpecs)
    def db_get_portSpecs(self):
        return self._db_portSpecs
    def db_add_portSpec(self, portSpec):
        self.is_dirty = True
        self._db_portSpecs.append(portSpec)
        self.db_portSpecs_id_index[portSpec.db_id] = portSpec
        self.db_portSpecs_name_index[(portSpec.db_name,portSpec.db_type)] = portSpec
    def db_change_portSpec(self, portSpec):
        self.is_dirty = True
        found = False
        for i in xrange(len(self._db_portSpecs)):
            if self._db_portSpecs[i].db_id == portSpec.db_id:
                self._db_portSpecs[i] = portSpec
                found = True
                break
        if not found:
            self._db_portSpecs.append(portSpec)
        self.db_portSpecs_id_index[portSpec.db_id] = portSpec
        self.db_portSpecs_name_index[(portSpec.db_name,portSpec.db_type)] = portSpec
    def db_delete_portSpec(self, portSpec):
        self.is_dirty = True
        for i in xrange(len(self._db_portSpecs)):
            if self._db_portSpecs[i].db_id == portSpec.db_id:
                if not self._db_portSpecs[i].is_new:
                    self.db_deleted_portSpecs.append(self._db_portSpecs[i])
                del self._db_portSpecs[i]
                break
        del self.db_portSpecs_id_index[portSpec.db_id]
        del self.db_portSpecs_name_index[(portSpec.db_name,portSpec.db_type)]
    def db_get_portSpec(self, key):
        for i in xrange(len(self._db_portSpecs)):
            if self._db_portSpecs[i].db_id == key:
                return self._db_portSpecs[i]
        return None
    def db_get_portSpec_by_id(self, key):
        return self.db_portSpecs_id_index[key]
    def db_has_portSpec_with_id(self, key):
        return key in self.db_portSpecs_id_index
    def db_get_portSpec_by_name(self, key):
        return self.db_portSpecs_name_index[key]
    def db_has_portSpec_with_name(self, key):
        return key in self.db_portSpecs_name_index
    
    def getPrimaryKey(self):
        return self._db_id

class DBTag(object):

    vtType = 'tag'

    def __init__(self, id=None, name=None):
        self._db_id = id
        self._db_name = name
        self.is_dirty = True
        self.is_new = True
    
    def __copy__(self):
        return DBTag.do_copy(self)

    def do_copy(self, new_ids=False, id_scope=None, id_remap=None):
        cp = DBTag(id=self._db_id,
                   name=self._db_name)
        
        # set new ids
        if new_ids:
            new_id = id_scope.getNewId(self.vtType)
            if self.vtType in id_scope.remap:
                id_remap[(id_scope.remap[self.vtType], self.db_id)] = new_id
            else:
                id_remap[(self.vtType, self.db_id)] = new_id
            cp.db_id = new_id
            if hasattr(self, 'db_id') and ('action', self._db_id) in id_remap:
                cp._db_id = id_remap[('action', self._db_id)]
        
        # recreate indices and set flags
        if not new_ids:
            cp.is_dirty = self.is_dirty
            cp.is_new = self.is_new
        return cp

    @staticmethod
    def update_version(old_obj, trans_dict, new_obj=None):
        if new_obj is None:
            new_obj = DBTag()
        class_dict = {}
        if new_obj.__class__.__name__ in trans_dict:
            class_dict = trans_dict[new_obj.__class__.__name__]
        if 'id' in class_dict:
            res = class_dict['id'](old_obj, trans_dict)
            new_obj.db_id = res
        elif hasattr(old_obj, 'db_id') and old_obj.db_id is not None:
            new_obj.db_id = old_obj.db_id
        if 'name' in class_dict:
            res = class_dict['name'](old_obj, trans_dict)
            new_obj.db_name = res
        elif hasattr(old_obj, 'db_name') and old_obj.db_name is not None:
            new_obj.db_name = old_obj.db_name
        new_obj.is_new = old_obj.is_new
        new_obj.is_dirty = old_obj.is_dirty
        return new_obj

    def db_children(self, parent=(None,None), orphan=False):
        return [(self, parent[0], parent[1])]
    def db_deleted_children(self, remove=False):
        children = []
        return children
    def has_changes(self):
        if self.is_dirty:
            return True
        return False
    def __get_db_id(self):
        return self._db_id
    def __set_db_id(self, id):
        self._db_id = id
        self.is_dirty = True
    db_id = property(__get_db_id, __set_db_id)
    def db_add_id(self, id):
        self._db_id = id
    def db_change_id(self, id):
        self._db_id = id
    def db_delete_id(self, id):
        self._db_id = None
    
    def __get_db_name(self):
        return self._db_name
    def __set_db_name(self, name):
        self._db_name = name
        self.is_dirty = True
    db_name = property(__get_db_name, __set_db_name)
    def db_add_name(self, name):
        self._db_name = name
    def db_change_name(self, name):
        self._db_name = name
    def db_delete_name(self, name):
        self._db_name = None
    
    def getPrimaryKey(self):
        return self._db_id

class DBPort(object):

    vtType = 'port'

    def __init__(self, id=None, type=None, moduleId=None, moduleName=None, name=None, signature=None):
        self._db_id = id
        self._db_type = type
        self._db_moduleId = moduleId
        self._db_moduleName = moduleName
        self._db_name = name
        self._db_signature = signature
        self.is_dirty = True
        self.is_new = True
    
    def __copy__(self):
        return DBPort.do_copy(self)

    def do_copy(self, new_ids=False, id_scope=None, id_remap=None):
        cp = DBPort(id=self._db_id,
                    type=self._db_type,
                    moduleId=self._db_moduleId,
                    moduleName=self._db_moduleName,
                    name=self._db_name,
                    signature=self._db_signature)
        
        # set new ids
        if new_ids:
            new_id = id_scope.getNewId(self.vtType)
            if self.vtType in id_scope.remap:
                id_remap[(id_scope.remap[self.vtType], self.db_id)] = new_id
            else:
                id_remap[(self.vtType, self.db_id)] = new_id
            cp.db_id = new_id
            if hasattr(self, 'db_moduleId') and ('module', self._db_moduleId) in id_remap:
                cp._db_moduleId = id_remap[('module', self._db_moduleId)]
        
        # recreate indices and set flags
        if not new_ids:
            cp.is_dirty = self.is_dirty
            cp.is_new = self.is_new
        return cp

    @staticmethod
    def update_version(old_obj, trans_dict, new_obj=None):
        if new_obj is None:
            new_obj = DBPort()
        class_dict = {}
        if new_obj.__class__.__name__ in trans_dict:
            class_dict = trans_dict[new_obj.__class__.__name__]
        if 'id' in class_dict:
            res = class_dict['id'](old_obj, trans_dict)
            new_obj.db_id = res
        elif hasattr(old_obj, 'db_id') and old_obj.db_id is not None:
            new_obj.db_id = old_obj.db_id
        if 'type' in class_dict:
            res = class_dict['type'](old_obj, trans_dict)
            new_obj.db_type = res
        elif hasattr(old_obj, 'db_type') and old_obj.db_type is not None:
            new_obj.db_type = old_obj.db_type
        if 'moduleId' in class_dict:
            res = class_dict['moduleId'](old_obj, trans_dict)
            new_obj.db_moduleId = res
        elif hasattr(old_obj, 'db_moduleId') and old_obj.db_moduleId is not None:
            new_obj.db_moduleId = old_obj.db_moduleId
        if 'moduleName' in class_dict:
            res = class_dict['moduleName'](old_obj, trans_dict)
            new_obj.db_moduleName = res
        elif hasattr(old_obj, 'db_moduleName') and old_obj.db_moduleName is not None:
            new_obj.db_moduleName = old_obj.db_moduleName
        if 'name' in class_dict:
            res = class_dict['name'](old_obj, trans_dict)
            new_obj.db_name = res
        elif hasattr(old_obj, 'db_name') and old_obj.db_name is not None:
            new_obj.db_name = old_obj.db_name
        if 'signature' in class_dict:
            res = class_dict['signature'](old_obj, trans_dict)
            new_obj.db_signature = res
        elif hasattr(old_obj, 'db_signature') and old_obj.db_signature is not None:
            new_obj.db_signature = old_obj.db_signature
        new_obj.is_new = old_obj.is_new
        new_obj.is_dirty = old_obj.is_dirty
        return new_obj

    def db_children(self, parent=(None,None), orphan=False):
        return [(self, parent[0], parent[1])]
    def db_deleted_children(self, remove=False):
        children = []
        return children
    def has_changes(self):
        if self.is_dirty:
            return True
        return False
    def __get_db_id(self):
        return self._db_id
    def __set_db_id(self, id):
        self._db_id = id
        self.is_dirty = True
    db_id = property(__get_db_id, __set_db_id)
    def db_add_id(self, id):
        self._db_id = id
    def db_change_id(self, id):
        self._db_id = id
    def db_delete_id(self, id):
        self._db_id = None
    
    def __get_db_type(self):
        return self._db_type
    def __set_db_type(self, type):
        self._db_type = type
        self.is_dirty = True
    db_type = property(__get_db_type, __set_db_type)
    def db_add_type(self, type):
        self._db_type = type
    def db_change_type(self, type):
        self._db_type = type
    def db_delete_type(self, type):
        self._db_type = None
    
    def __get_db_moduleId(self):
        return self._db_moduleId
    def __set_db_moduleId(self, moduleId):
        self._db_moduleId = moduleId
        self.is_dirty = True
    db_moduleId = property(__get_db_moduleId, __set_db_moduleId)
    def db_add_moduleId(self, moduleId):
        self._db_moduleId = moduleId
    def db_change_moduleId(self, moduleId):
        self._db_moduleId = moduleId
    def db_delete_moduleId(self, moduleId):
        self._db_moduleId = None
    
    def __get_db_moduleName(self):
        return self._db_moduleName
    def __set_db_moduleName(self, moduleName):
        self._db_moduleName = moduleName
        self.is_dirty = True
    db_moduleName = property(__get_db_moduleName, __set_db_moduleName)
    def db_add_moduleName(self, moduleName):
        self._db_moduleName = moduleName
    def db_change_moduleName(self, moduleName):
        self._db_moduleName = moduleName
    def db_delete_moduleName(self, moduleName):
        self._db_moduleName = None
    
    def __get_db_name(self):
        return self._db_name
    def __set_db_name(self, name):
        self._db_name = name
        self.is_dirty = True
    db_name = property(__get_db_name, __set_db_name)
    def db_add_name(self, name):
        self._db_name = name
    def db_change_name(self, name):
        self._db_name = name
    def db_delete_name(self, name):
        self._db_name = None
    
    def __get_db_signature(self):
        return self._db_signature
    def __set_db_signature(self, signature):
        self._db_signature = signature
        self.is_dirty = True
    db_signature = property(__get_db_signature, __set_db_signature)
    def db_add_signature(self, signature):
        self._db_signature = signature
    def db_change_signature(self, signature):
        self._db_signature = signature
    def db_delete_signature(self, signature):
        self._db_signature = None
    
    def getPrimaryKey(self):
        return self._db_id

class DBMachine(object):

    vtType = 'machine'

    def __init__(self, id=None, name=None, os=None, architecture=None, processor=None, ram=None):
        self._db_id = id
        self._db_name = name
        self._db_os = os
        self._db_architecture = architecture
        self._db_processor = processor
        self._db_ram = ram
        self.is_dirty = True
        self.is_new = True
    
    def __copy__(self):
        return DBMachine.do_copy(self)

    def do_copy(self, new_ids=False, id_scope=None, id_remap=None):
        cp = DBMachine(id=self._db_id,
                       name=self._db_name,
                       os=self._db_os,
                       architecture=self._db_architecture,
                       processor=self._db_processor,
                       ram=self._db_ram)
        
        # set new ids
        if new_ids:
            new_id = id_scope.getNewId(self.vtType)
            if self.vtType in id_scope.remap:
                id_remap[(id_scope.remap[self.vtType], self.db_id)] = new_id
            else:
                id_remap[(self.vtType, self.db_id)] = new_id
            cp.db_id = new_id
            if hasattr(self, 'db_vistrailId') and ('vistrail', self._db_vistrailId) in id_remap:
                cp._db_vistrailId = id_remap[('vistrail', self._db_vistrailId)]
        
        # recreate indices and set flags
        if not new_ids:
            cp.is_dirty = self.is_dirty
            cp.is_new = self.is_new
        return cp

    @staticmethod
    def update_version(old_obj, trans_dict, new_obj=None):
        if new_obj is None:
            new_obj = DBMachine()
        class_dict = {}
        if new_obj.__class__.__name__ in trans_dict:
            class_dict = trans_dict[new_obj.__class__.__name__]
        if 'id' in class_dict:
            res = class_dict['id'](old_obj, trans_dict)
            new_obj.db_id = res
        elif hasattr(old_obj, 'db_id') and old_obj.db_id is not None:
            new_obj.db_id = old_obj.db_id
        if 'name' in class_dict:
            res = class_dict['name'](old_obj, trans_dict)
            new_obj.db_name = res
        elif hasattr(old_obj, 'db_name') and old_obj.db_name is not None:
            new_obj.db_name = old_obj.db_name
        if 'os' in class_dict:
            res = class_dict['os'](old_obj, trans_dict)
            new_obj.db_os = res
        elif hasattr(old_obj, 'db_os') and old_obj.db_os is not None:
            new_obj.db_os = old_obj.db_os
        if 'architecture' in class_dict:
            res = class_dict['architecture'](old_obj, trans_dict)
            new_obj.db_architecture = res
        elif hasattr(old_obj, 'db_architecture') and old_obj.db_architecture is not None:
            new_obj.db_architecture = old_obj.db_architecture
        if 'processor' in class_dict:
            res = class_dict['processor'](old_obj, trans_dict)
            new_obj.db_processor = res
        elif hasattr(old_obj, 'db_processor') and old_obj.db_processor is not None:
            new_obj.db_processor = old_obj.db_processor
        if 'ram' in class_dict:
            res = class_dict['ram'](old_obj, trans_dict)
            new_obj.db_ram = res
        elif hasattr(old_obj, 'db_ram') and old_obj.db_ram is not None:
            new_obj.db_ram = old_obj.db_ram
        new_obj.is_new = old_obj.is_new
        new_obj.is_dirty = old_obj.is_dirty
        return new_obj

    def db_children(self, parent=(None,None), orphan=False):
        return [(self, parent[0], parent[1])]
    def db_deleted_children(self, remove=False):
        children = []
        return children
    def has_changes(self):
        if self.is_dirty:
            return True
        return False
    def __get_db_id(self):
        return self._db_id
    def __set_db_id(self, id):
        self._db_id = id
        self.is_dirty = True
    db_id = property(__get_db_id, __set_db_id)
    def db_add_id(self, id):
        self._db_id = id
    def db_change_id(self, id):
        self._db_id = id
    def db_delete_id(self, id):
        self._db_id = None
    
    def __get_db_name(self):
        return self._db_name
    def __set_db_name(self, name):
        self._db_name = name
        self.is_dirty = True
    db_name = property(__get_db_name, __set_db_name)
    def db_add_name(self, name):
        self._db_name = name
    def db_change_name(self, name):
        self._db_name = name
    def db_delete_name(self, name):
        self._db_name = None
    
    def __get_db_os(self):
        return self._db_os
    def __set_db_os(self, os):
        self._db_os = os
        self.is_dirty = True
    db_os = property(__get_db_os, __set_db_os)
    def db_add_os(self, os):
        self._db_os = os
    def db_change_os(self, os):
        self._db_os = os
    def db_delete_os(self, os):
        self._db_os = None
    
    def __get_db_architecture(self):
        return self._db_architecture
    def __set_db_architecture(self, architecture):
        self._db_architecture = architecture
        self.is_dirty = True
    db_architecture = property(__get_db_architecture, __set_db_architecture)
    def db_add_architecture(self, architecture):
        self._db_architecture = architecture
    def db_change_architecture(self, architecture):
        self._db_architecture = architecture
    def db_delete_architecture(self, architecture):
        self._db_architecture = None
    
    def __get_db_processor(self):
        return self._db_processor
    def __set_db_processor(self, processor):
        self._db_processor = processor
        self.is_dirty = True
    db_processor = property(__get_db_processor, __set_db_processor)
    def db_add_processor(self, processor):
        self._db_processor = processor
    def db_change_processor(self, processor):
        self._db_processor = processor
    def db_delete_processor(self, processor):
        self._db_processor = None
    
    def __get_db_ram(self):
        return self._db_ram
    def __set_db_ram(self, ram):
        self._db_ram = ram
        self.is_dirty = True
    db_ram = property(__get_db_ram, __set_db_ram)
    def db_add_ram(self, ram):
        self._db_ram = ram
    def db_change_ram(self, ram):
        self._db_ram = ram
    def db_delete_ram(self, ram):
        self._db_ram = None
    
    def getPrimaryKey(self):
        return self._db_id

class DBOther(object):

    vtType = 'other'

    def __init__(self, id=None, key=None, value=None):
        self._db_id = id
        self._db_key = key
        self._db_value = value
        self.is_dirty = True
        self.is_new = True
    
    def __copy__(self):
        return DBOther.do_copy(self)

    def do_copy(self, new_ids=False, id_scope=None, id_remap=None):
        cp = DBOther(id=self._db_id,
                     key=self._db_key,
                     value=self._db_value)
        
        # set new ids
        if new_ids:
            new_id = id_scope.getNewId(self.vtType)
            if self.vtType in id_scope.remap:
                id_remap[(id_scope.remap[self.vtType], self.db_id)] = new_id
            else:
                id_remap[(self.vtType, self.db_id)] = new_id
            cp.db_id = new_id
        
        # recreate indices and set flags
        if not new_ids:
            cp.is_dirty = self.is_dirty
            cp.is_new = self.is_new
        return cp

    @staticmethod
    def update_version(old_obj, trans_dict, new_obj=None):
        if new_obj is None:
            new_obj = DBOther()
        class_dict = {}
        if new_obj.__class__.__name__ in trans_dict:
            class_dict = trans_dict[new_obj.__class__.__name__]
        if 'id' in class_dict:
            res = class_dict['id'](old_obj, trans_dict)
            new_obj.db_id = res
        elif hasattr(old_obj, 'db_id') and old_obj.db_id is not None:
            new_obj.db_id = old_obj.db_id
        if 'key' in class_dict:
            res = class_dict['key'](old_obj, trans_dict)
            new_obj.db_key = res
        elif hasattr(old_obj, 'db_key') and old_obj.db_key is not None:
            new_obj.db_key = old_obj.db_key
        if 'value' in class_dict:
            res = class_dict['value'](old_obj, trans_dict)
            new_obj.db_value = res
        elif hasattr(old_obj, 'db_value') and old_obj.db_value is not None:
            new_obj.db_value = old_obj.db_value
        new_obj.is_new = old_obj.is_new
        new_obj.is_dirty = old_obj.is_dirty
        return new_obj

    def db_children(self, parent=(None,None), orphan=False):
        return [(self, parent[0], parent[1])]
    def db_deleted_children(self, remove=False):
        children = []
        return children
    def has_changes(self):
        if self.is_dirty:
            return True
        return False
    def __get_db_id(self):
        return self._db_id
    def __set_db_id(self, id):
        self._db_id = id
        self.is_dirty = True
    db_id = property(__get_db_id, __set_db_id)
    def db_add_id(self, id):
        self._db_id = id
    def db_change_id(self, id):
        self._db_id = id
    def db_delete_id(self, id):
        self._db_id = None
    
    def __get_db_key(self):
        return self._db_key
    def __set_db_key(self, key):
        self._db_key = key
        self.is_dirty = True
    db_key = property(__get_db_key, __set_db_key)
    def db_add_key(self, key):
        self._db_key = key
    def db_change_key(self, key):
        self._db_key = key
    def db_delete_key(self, key):
        self._db_key = None
    
    def __get_db_value(self):
        return self._db_value
    def __set_db_value(self, value):
        self._db_value = value
        self.is_dirty = True
    db_value = property(__get_db_value, __set_db_value)
    def db_add_value(self, value):
        self._db_value = value
    def db_change_value(self, value):
        self._db_value = value
    def db_delete_value(self, value):
        self._db_value = None
    
    def getPrimaryKey(self):
        return self._db_id

class DBLocation(object):

    vtType = 'location'

    def __init__(self, id=None, x=None, y=None):
        self._db_id = id
        self._db_x = x
        self._db_y = y
        self.is_dirty = True
        self.is_new = True
    
    def __copy__(self):
        return DBLocation.do_copy(self)

    def do_copy(self, new_ids=False, id_scope=None, id_remap=None):
        cp = DBLocation(id=self._db_id,
                        x=self._db_x,
                        y=self._db_y)
        
        # set new ids
        if new_ids:
            new_id = id_scope.getNewId(self.vtType)
            if self.vtType in id_scope.remap:
                id_remap[(id_scope.remap[self.vtType], self.db_id)] = new_id
            else:
                id_remap[(self.vtType, self.db_id)] = new_id
            cp.db_id = new_id
        
        # recreate indices and set flags
        if not new_ids:
            cp.is_dirty = self.is_dirty
            cp.is_new = self.is_new
        return cp

    @staticmethod
    def update_version(old_obj, trans_dict, new_obj=None):
        if new_obj is None:
            new_obj = DBLocation()
        class_dict = {}
        if new_obj.__class__.__name__ in trans_dict:
            class_dict = trans_dict[new_obj.__class__.__name__]
        if 'id' in class_dict:
            res = class_dict['id'](old_obj, trans_dict)
            new_obj.db_id = res
        elif hasattr(old_obj, 'db_id') and old_obj.db_id is not None:
            new_obj.db_id = old_obj.db_id
        if 'x' in class_dict:
            res = class_dict['x'](old_obj, trans_dict)
            new_obj.db_x = res
        elif hasattr(old_obj, 'db_x') and old_obj.db_x is not None:
            new_obj.db_x = old_obj.db_x
        if 'y' in class_dict:
            res = class_dict['y'](old_obj, trans_dict)
            new_obj.db_y = res
        elif hasattr(old_obj, 'db_y') and old_obj.db_y is not None:
            new_obj.db_y = old_obj.db_y
        new_obj.is_new = old_obj.is_new
        new_obj.is_dirty = old_obj.is_dirty
        return new_obj

    def db_children(self, parent=(None,None), orphan=False):
        return [(self, parent[0], parent[1])]
    def db_deleted_children(self, remove=False):
        children = []
        return children
    def has_changes(self):
        if self.is_dirty:
            return True
        return False
    def __get_db_id(self):
        return self._db_id
    def __set_db_id(self, id):
        self._db_id = id
        self.is_dirty = True
    db_id = property(__get_db_id, __set_db_id)
    def db_add_id(self, id):
        self._db_id = id
    def db_change_id(self, id):
        self._db_id = id
    def db_delete_id(self, id):
        self._db_id = None
    
    def __get_db_x(self):
        return self._db_x
    def __set_db_x(self, x):
        self._db_x = x
        self.is_dirty = True
    db_x = property(__get_db_x, __set_db_x)
    def db_add_x(self, x):
        self._db_x = x
    def db_change_x(self, x):
        self._db_x = x
    def db_delete_x(self, x):
        self._db_x = None
    
    def __get_db_y(self):
        return self._db_y
    def __set_db_y(self, y):
        self._db_y = y
        self.is_dirty = True
    db_y = property(__get_db_y, __set_db_y)
    def db_add_y(self, y):
        self._db_y = y
    def db_change_y(self, y):
        self._db_y = y
    def db_delete_y(self, y):
        self._db_y = None
    
    def getPrimaryKey(self):
        return self._db_id

class DBParameter(object):

    vtType = 'parameter'

    def __init__(self, id=None, pos=None, name=None, type=None, val=None, alias=None):
        self._db_id = id
        self._db_pos = pos
        self._db_name = name
        self._db_type = type
        self._db_val = val
        self._db_alias = alias
        self.is_dirty = True
        self.is_new = True
    
    def __copy__(self):
        return DBParameter.do_copy(self)

    def do_copy(self, new_ids=False, id_scope=None, id_remap=None):
        cp = DBParameter(id=self._db_id,
                         pos=self._db_pos,
                         name=self._db_name,
                         type=self._db_type,
                         val=self._db_val,
                         alias=self._db_alias)
        
        # set new ids
        if new_ids:
            new_id = id_scope.getNewId(self.vtType)
            if self.vtType in id_scope.remap:
                id_remap[(id_scope.remap[self.vtType], self.db_id)] = new_id
            else:
                id_remap[(self.vtType, self.db_id)] = new_id
            cp.db_id = new_id
        
        # recreate indices and set flags
        if not new_ids:
            cp.is_dirty = self.is_dirty
            cp.is_new = self.is_new
        return cp

    @staticmethod
    def update_version(old_obj, trans_dict, new_obj=None):
        if new_obj is None:
            new_obj = DBParameter()
        class_dict = {}
        if new_obj.__class__.__name__ in trans_dict:
            class_dict = trans_dict[new_obj.__class__.__name__]
        if 'id' in class_dict:
            res = class_dict['id'](old_obj, trans_dict)
            new_obj.db_id = res
        elif hasattr(old_obj, 'db_id') and old_obj.db_id is not None:
            new_obj.db_id = old_obj.db_id
        if 'pos' in class_dict:
            res = class_dict['pos'](old_obj, trans_dict)
            new_obj.db_pos = res
        elif hasattr(old_obj, 'db_pos') and old_obj.db_pos is not None:
            new_obj.db_pos = old_obj.db_pos
        if 'name' in class_dict:
            res = class_dict['name'](old_obj, trans_dict)
            new_obj.db_name = res
        elif hasattr(old_obj, 'db_name') and old_obj.db_name is not None:
            new_obj.db_name = old_obj.db_name
        if 'type' in class_dict:
            res = class_dict['type'](old_obj, trans_dict)
            new_obj.db_type = res
        elif hasattr(old_obj, 'db_type') and old_obj.db_type is not None:
            new_obj.db_type = old_obj.db_type
        if 'val' in class_dict:
            res = class_dict['val'](old_obj, trans_dict)
            new_obj.db_val = res
        elif hasattr(old_obj, 'db_val') and old_obj.db_val is not None:
            new_obj.db_val = old_obj.db_val
        if 'alias' in class_dict:
            res = class_dict['alias'](old_obj, trans_dict)
            new_obj.db_alias = res
        elif hasattr(old_obj, 'db_alias') and old_obj.db_alias is not None:
            new_obj.db_alias = old_obj.db_alias
        new_obj.is_new = old_obj.is_new
        new_obj.is_dirty = old_obj.is_dirty
        return new_obj

    def db_children(self, parent=(None,None), orphan=False):
        return [(self, parent[0], parent[1])]
    def db_deleted_children(self, remove=False):
        children = []
        return children
    def has_changes(self):
        if self.is_dirty:
            return True
        return False
    def __get_db_id(self):
        return self._db_id
    def __set_db_id(self, id):
        self._db_id = id
        self.is_dirty = True
    db_id = property(__get_db_id, __set_db_id)
    def db_add_id(self, id):
        self._db_id = id
    def db_change_id(self, id):
        self._db_id = id
    def db_delete_id(self, id):
        self._db_id = None
    
    def __get_db_pos(self):
        return self._db_pos
    def __set_db_pos(self, pos):
        self._db_pos = pos
        self.is_dirty = True
    db_pos = property(__get_db_pos, __set_db_pos)
    def db_add_pos(self, pos):
        self._db_pos = pos
    def db_change_pos(self, pos):
        self._db_pos = pos
    def db_delete_pos(self, pos):
        self._db_pos = None
    
    def __get_db_name(self):
        return self._db_name
    def __set_db_name(self, name):
        self._db_name = name
        self.is_dirty = True
    db_name = property(__get_db_name, __set_db_name)
    def db_add_name(self, name):
        self._db_name = name
    def db_change_name(self, name):
        self._db_name = name
    def db_delete_name(self, name):
        self._db_name = None
    
    def __get_db_type(self):
        return self._db_type
    def __set_db_type(self, type):
        self._db_type = type
        self.is_dirty = True
    db_type = property(__get_db_type, __set_db_type)
    def db_add_type(self, type):
        self._db_type = type
    def db_change_type(self, type):
        self._db_type = type
    def db_delete_type(self, type):
        self._db_type = None
    
    def __get_db_val(self):
        return self._db_val
    def __set_db_val(self, val):
        self._db_val = val
        self.is_dirty = True
    db_val = property(__get_db_val, __set_db_val)
    def db_add_val(self, val):
        self._db_val = val
    def db_change_val(self, val):
        self._db_val = val
    def db_delete_val(self, val):
        self._db_val = None
    
    def __get_db_alias(self):
        return self._db_alias
    def __set_db_alias(self, alias):
        self._db_alias = alias
        self.is_dirty = True
    db_alias = property(__get_db_alias, __set_db_alias)
    def db_add_alias(self, alias):
        self._db_alias = alias
    def db_change_alias(self, alias):
        self._db_alias = alias
    def db_delete_alias(self, alias):
        self._db_alias = None
    
    def getPrimaryKey(self):
        return self._db_id

class DBPluginData(object):

    vtType = 'plugin_data'

    def __init__(self, id=None, data=None):
        self._db_id = id
        self._db_data = data
        self.is_dirty = True
        self.is_new = True
    
    def __copy__(self):
        return DBPluginData.do_copy(self)

    def do_copy(self, new_ids=False, id_scope=None, id_remap=None):
        cp = DBPluginData(id=self._db_id,
                          data=self._db_data)
        
        # set new ids
        if new_ids:
            new_id = id_scope.getNewId(self.vtType)
            if self.vtType in id_scope.remap:
                id_remap[(id_scope.remap[self.vtType], self.db_id)] = new_id
            else:
                id_remap[(self.vtType, self.db_id)] = new_id
            cp.db_id = new_id
        
        # recreate indices and set flags
        if not new_ids:
            cp.is_dirty = self.is_dirty
            cp.is_new = self.is_new
        return cp

    @staticmethod
    def update_version(old_obj, trans_dict, new_obj=None):
        if new_obj is None:
            new_obj = DBPluginData()
        class_dict = {}
        if new_obj.__class__.__name__ in trans_dict:
            class_dict = trans_dict[new_obj.__class__.__name__]
        if 'id' in class_dict:
            res = class_dict['id'](old_obj, trans_dict)
            new_obj.db_id = res
        elif hasattr(old_obj, 'db_id') and old_obj.db_id is not None:
            new_obj.db_id = old_obj.db_id
        if 'data' in class_dict:
            res = class_dict['data'](old_obj, trans_dict)
            new_obj.db_data = res
        elif hasattr(old_obj, 'db_data') and old_obj.db_data is not None:
            new_obj.db_data = old_obj.db_data
        new_obj.is_new = old_obj.is_new
        new_obj.is_dirty = old_obj.is_dirty
        return new_obj

    def db_children(self, parent=(None,None), orphan=False):
        return [(self, parent[0], parent[1])]
    def db_deleted_children(self, remove=False):
        children = []
        return children
    def has_changes(self):
        if self.is_dirty:
            return True
        return False
    def __get_db_id(self):
        return self._db_id
    def __set_db_id(self, id):
        self._db_id = id
        self.is_dirty = True
    db_id = property(__get_db_id, __set_db_id)
    def db_add_id(self, id):
        self._db_id = id
    def db_change_id(self, id):
        self._db_id = id
    def db_delete_id(self, id):
        self._db_id = None
    
    def __get_db_data(self):
        return self._db_data
    def __set_db_data(self, data):
        self._db_data = data
        self.is_dirty = True
    db_data = property(__get_db_data, __set_db_data)
    def db_add_data(self, data):
        self._db_data = data
    def db_change_data(self, data):
        self._db_data = data
    def db_delete_data(self, data):
        self._db_data = None
    
    def getPrimaryKey(self):
        return self._db_id

class DBFunction(object):

    vtType = 'function'

    def __init__(self, id=None, pos=None, name=None, parameters=None):
        self._db_id = id
        self._db_pos = pos
        self._db_name = name
        self.db_deleted_parameters = []
        self.db_parameters_id_index = {}
        if parameters is None:
            self._db_parameters = []
        else:
            self._db_parameters = parameters
            for v in self._db_parameters:
                self.db_parameters_id_index[v.db_id] = v
        self.is_dirty = True
        self.is_new = True
    
    def __copy__(self):
        return DBFunction.do_copy(self)

    def do_copy(self, new_ids=False, id_scope=None, id_remap=None):
        cp = DBFunction(id=self._db_id,
                        pos=self._db_pos,
                        name=self._db_name)
        if self._db_parameters is None:
            cp._db_parameters = []
        else:
            cp._db_parameters = [v.do_copy(new_ids, id_scope, id_remap) for v in self._db_parameters]
        
        # set new ids
        if new_ids:
            new_id = id_scope.getNewId(self.vtType)
            if self.vtType in id_scope.remap:
                id_remap[(id_scope.remap[self.vtType], self.db_id)] = new_id
            else:
                id_remap[(self.vtType, self.db_id)] = new_id
            cp.db_id = new_id
        
        # recreate indices and set flags
        cp.db_parameters_id_index = dict((v.db_id, v) for v in cp._db_parameters)
        if not new_ids:
            cp.is_dirty = self.is_dirty
            cp.is_new = self.is_new
        return cp

    @staticmethod
    def update_version(old_obj, trans_dict, new_obj=None):
        if new_obj is None:
            new_obj = DBFunction()
        class_dict = {}
        if new_obj.__class__.__name__ in trans_dict:
            class_dict = trans_dict[new_obj.__class__.__name__]
        if 'id' in class_dict:
            res = class_dict['id'](old_obj, trans_dict)
            new_obj.db_id = res
        elif hasattr(old_obj, 'db_id') and old_obj.db_id is not None:
            new_obj.db_id = old_obj.db_id
        if 'pos' in class_dict:
            res = class_dict['pos'](old_obj, trans_dict)
            new_obj.db_pos = res
        elif hasattr(old_obj, 'db_pos') and old_obj.db_pos is not None:
            new_obj.db_pos = old_obj.db_pos
        if 'name' in class_dict:
            res = class_dict['name'](old_obj, trans_dict)
            new_obj.db_name = res
        elif hasattr(old_obj, 'db_name') and old_obj.db_name is not None:
            new_obj.db_name = old_obj.db_name
        if 'parameters' in class_dict:
            res = class_dict['parameters'](old_obj, trans_dict)
            for obj in res:
                new_obj.db_add_parameter(obj)
        elif hasattr(old_obj, 'db_parameters') and old_obj.db_parameters is not None:
            for obj in old_obj.db_parameters:
                new_obj.db_add_parameter(DBParameter.update_version(obj, trans_dict))
        if hasattr(old_obj, 'db_deleted_parameters') and hasattr(new_obj, 'db_deleted_parameters'):
            for obj in old_obj.db_deleted_parameters:
                n_obj = DBParameter.update_version(obj, trans_dict)
                new_obj.db_deleted_parameters.append(n_obj)
        new_obj.is_new = old_obj.is_new
        new_obj.is_dirty = old_obj.is_dirty
        return new_obj

    def db_children(self, parent=(None,None), orphan=False):
        children = []
        to_del = []
        for child in self.db_parameters:
            children.extend(child.db_children((self.vtType, self.db_id), orphan))
            if orphan:
                to_del.append(child)
        for child in to_del:
            self.db_delete_parameter(child)
        children.append((self, parent[0], parent[1]))
        return children
    def db_deleted_children(self, remove=False):
        children = []
        children.extend(self.db_deleted_parameters)
        if remove:
            self.db_deleted_parameters = []
        return children
    def has_changes(self):
        if self.is_dirty:
            return True
        for child in self._db_parameters:
            if child.has_changes():
                return True
        return False
    def __get_db_id(self):
        return self._db_id
    def __set_db_id(self, id):
        self._db_id = id
        self.is_dirty = True
    db_id = property(__get_db_id, __set_db_id)
    def db_add_id(self, id):
        self._db_id = id
    def db_change_id(self, id):
        self._db_id = id
    def db_delete_id(self, id):
        self._db_id = None
    
    def __get_db_pos(self):
        return self._db_pos
    def __set_db_pos(self, pos):
        self._db_pos = pos
        self.is_dirty = True
    db_pos = property(__get_db_pos, __set_db_pos)
    def db_add_pos(self, pos):
        self._db_pos = pos
    def db_change_pos(self, pos):
        self._db_pos = pos
    def db_delete_pos(self, pos):
        self._db_pos = None
    
    def __get_db_name(self):
        return self._db_name
    def __set_db_name(self, name):
        self._db_name = name
        self.is_dirty = True
    db_name = property(__get_db_name, __set_db_name)
    def db_add_name(self, name):
        self._db_name = name
    def db_change_name(self, name):
        self._db_name = name
    def db_delete_name(self, name):
        self._db_name = None
    
    def __get_db_parameters(self):
        return self._db_parameters
    def __set_db_parameters(self, parameters):
        self._db_parameters = parameters
        self.is_dirty = True
    db_parameters = property(__get_db_parameters, __set_db_parameters)
    def db_get_parameters(self):
        return self._db_parameters
    def db_add_parameter(self, parameter):
        self.is_dirty = True
        self._db_parameters.append(parameter)
        self.db_parameters_id_index[parameter.db_id] = parameter
    def db_change_parameter(self, parameter):
        self.is_dirty = True
        found = False
        for i in xrange(len(self._db_parameters)):
            if self._db_parameters[i].db_id == parameter.db_id:
                self._db_parameters[i] = parameter
                found = True
                break
        if not found:
            self._db_parameters.append(parameter)
        self.db_parameters_id_index[parameter.db_id] = parameter
    def db_delete_parameter(self, parameter):
        self.is_dirty = True
        for i in xrange(len(self._db_parameters)):
            if self._db_parameters[i].db_id == parameter.db_id:
                if not self._db_parameters[i].is_new:
                    self.db_deleted_parameters.append(self._db_parameters[i])
                del self._db_parameters[i]
                break
        del self.db_parameters_id_index[parameter.db_id]
    def db_get_parameter(self, key):
        for i in xrange(len(self._db_parameters)):
            if self._db_parameters[i].db_id == key:
                return self._db_parameters[i]
        return None
    def db_get_parameter_by_id(self, key):
        return self.db_parameters_id_index[key]
    def db_has_parameter_with_id(self, key):
        return key in self.db_parameters_id_index
    
    def getPrimaryKey(self):
        return self._db_id