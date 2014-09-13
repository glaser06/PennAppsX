//
//  AppDelegate.swift
//  MusicNotifApp
//
//  Created by Zaizen Kaegyoshi on 9/13/14.
//  Copyright (c) 2014 Zaizen Kaegyoshi. All rights reserved.
//

import Cocoa

class AppDelegate: NSObject, NSApplicationDelegate,NSSpeechRecognizerDelegate {
    
    @IBOutlet weak var window: NSWindow!
    @IBOutlet weak var theLabel: NSTextField!
    @IBOutlet weak var theButton: NSButton!
    
    var buttonPresses = 0;
    
    var statusBar = NSStatusBar.systemStatusBar()
    var statusBarItem : NSStatusItem = NSStatusItem()
    var menu: NSMenu = NSMenu()
    var menuItem : NSMenuItem = NSMenuItem()
    var listen: NSSpeechRecognizer!
    var name: String!
    override func awakeFromNib() {
        theLabel.stringValue = "You've pressed the button \n \(buttonPresses) times!"
        
        //Add statusBarItem
        statusBarItem = statusBar.statusItemWithLength(-1)
        statusBarItem.menu = menu
        statusBarItem.title = "Music"
        
        //Add menuItem to menu
        menuItem.title = "Setting"
        menuItem.action = Selector("setWindowVisible:")
        menuItem.keyEquivalent = ""
        menu.addItem(menuItem)
    }
    
    func applicationDidFinishLaunching(aNotification: NSNotification?) {
        listen = NSSpeechRecognizer()
        var cmds = ["sunny","something","yousef","gerry","kumail"]
        
        listen.commands = cmds
        listen.listensInForegroundOnly = false
        listen.blocksOtherRecognizers = true
        listen.delegate = self
        listen.startListening()
        
        self.window!.orderOut(self)
    }
    
    func speechRecognizer(sender: NSSpeechRecognizer!, didRecognizeCommand command: AnyObject!) {
        print("\(command as String) is talking to you \n")
    }
    
    @IBAction func buttonPressed(sender: NSButton) {
        buttonPresses+=1
        theLabel.stringValue = "Enter the closest English pronounciation of your name"
        //menuItem.title = "Clicked \(buttonPresses)"
        listen.stopListening()
        statusBarItem.title = "Listen"
    }
    
    func setWindowVisible(sender: AnyObject){
        self.window!.orderFront(self)
    }
}
