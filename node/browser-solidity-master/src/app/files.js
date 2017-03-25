'use strict'

var EventManager = require('../lib/eventManager')

function Files (storage) {
  var event = new EventManager()
  this.event = event
  var readonly = {}

  this.exists = function (path) {
    // NOTE: ignore the config file
    if (path === '.remix.config') {
      return false
    }

    return this.isReadOnly(path) || storage.exists(path)
  }

  this.get = function (path) {
    // NOTE: ignore the config file
    if (path === '.remix.config') {
      return null
    }

    return readonly[path] || storage.get(path)
  }

  this.set = function (path, content) {
    // NOTE: ignore the config file
    if (path === '.remix.config') {
      return false
    }

    if (!this.isReadOnly(path)) {
      var exists = storage.exists(path)
      if (!storage.set(path, content)) {
        return false
      }
      if (!exists) {
        event.trigger('fileAdded', [path, false])
      } else {
        event.trigger('fileChanged', [path])
      }
      return true
    }

    return false
  }

  this.addReadOnly = function (path, content) {
    if (!storage.exists(path)) {
      readonly[path] = content
      event.trigger('fileAdded', [path, true])
      return true
    }

    return false
  }

  this.isReadOnly = function (path) {
    return readonly[path] !== undefined
  }

  this.remove = function (path) {
    if (!this.exists(path)) {
      return false
    }

    if (this.isReadOnly(path)) {
      readonly[path] = undefined
    } else {
      if (!storage.remove(path)) {
        return false
      }
    }
    event.trigger('fileRemoved', [path])
    return true
  }

  this.rename = function (oldPath, newPath) {
    if (!this.isReadOnly(oldPath) && storage.exists(oldPath)) {
      if (!storage.rename(oldPath, newPath)) {
        return false
      }
      event.trigger('fileRenamed', [oldPath, newPath])
      return true
    }
    return false
  }

  this.list = function () {
    var files = {}

    // add r/w files to the list
    storage.keys().forEach(function (path) {
      // NOTE: as a temporary measure do not show the config file
      if (path !== '.remix.config') {
        files[path] = false
      }
    })

    // add r/o files to the list
    Object.keys(readonly).forEach(function (path) {
      files[path] = true
    })

    return files
  }

  // rename .browser-solidity.json to .remix.config
  if (this.exists('.browser-solidity.json')) {
    this.rename('.browser-solidity.json', '.remix.config')
  }
}

module.exports = Files
