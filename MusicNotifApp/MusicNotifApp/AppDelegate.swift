//
//  AppDelegate.swift
//  MusicNotifApp
//
//  Created by Zaizen Kaegyoshi on 9/12/14.
//  Copyright (c) 2014 Zaizen Kaegyoshi. All rights reserved.
//

import Cocoa

class AppDelegate: NSObject, NSApplicationDelegate {
    
    @IBOutlet weak var window: NSWindow!
    @IBOutlet weak var theLabel: NSTextField!
    @IBOutlet weak var theButton: NSButton!
    
    var buttonPresses = 0;
    
    var statusBar = NSStatusBar.systemStatusBar()
    var statusBarItem : NSStatusItem = NSStatusItem()
    var menu: NSMenu = NSMenu()
    var menuItem : NSMenuItem = NSMenuItem()
    
    override func awakeFromNib() {
        theLabel.stringValue = "You've pressed the button \n \(buttonPresses) times!"
        
        //Add statusBarItem
        statusBarItem = statusBar.statusItemWithLength(-1)
        statusBarItem.menu = menu
        statusBarItem.title = "MusicNotif"
        
        //Add menuItem to menu
        menuItem.title = "Clicked"
        menuItem.action = Selector("setWindowVisible:")
        menuItem.keyEquivalent = ""
        menu.addItem(menuItem)
    }
    
    func applicationDidFinishLaunching(aNotification: NSNotification?) {
        var listen: NSSpeechRecognizer!
        var cmds = ["Something"]
        
        self.window!.orderOut(self)
    }
    
    @IBAction func buttonPressed(sender: NSButton) {
        buttonPresses+=1
        theLabel.stringValue = "You've pressed the button \n \(buttonPresses) times!"
        menuItem.title = "Clicked \(buttonPresses)"
        statusBarItem.title = "MusicNotif"
    }
    
    func setWindowVisible(sender: AnyObject){
        self.window!.orderFront(self)
    }
}

