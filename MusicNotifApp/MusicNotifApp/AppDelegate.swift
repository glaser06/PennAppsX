//
//  AppDelegate.swift
//  MusicNotifApp
//
//  Created by Zaizen Kaegyoshi on 9/13/14.
//  Copyright (c) 2014 Zaizen Kaegyoshi. All rights reserved.
//

import Cocoa
import Foundation

class AppDelegate: NSObject, NSApplicationDelegate,NSSpeechRecognizerDelegate {
    
    @IBOutlet weak var window: NSWindow!
    @IBOutlet weak var theLabel: NSTextField!
    @IBOutlet weak var theButton: NSButton!
    
    var buttonPresses = 0;
    
    @IBOutlet weak var nameText: NSTextField!
    var statusBar = NSStatusBar.systemStatusBar()
    var statusBarItem : NSStatusItem = NSStatusItem()
    var menu: NSMenu = NSMenu()
    var menuItem : NSMenuItem = NSMenuItem()
    var listen: NSSpeechRecognizer!
    var name: String!
    override func awakeFromNib() {
        //theLabel.stringValue = "You've pressed the button \n \(buttonPresses) times!"
        
        //Add statusBarItem
        statusBarItem = statusBar.statusItemWithLength(-1)
        statusBarItem.menu = menu
        statusBarItem.title = "Music"
        
        //Add menuItem to menu
        menuItem.title = "Setting"
        menuItem.action = Selector("setWindowVisible:")
        menuItem.keyEquivalent = ""
        menu.addItem(menuItem)
        
        setWindowVisible(self)
        
        
    }
    
    func applicationDidFinishLaunching(aNotification: NSNotification?) {
        
        name = "";
        if(name != "")
        {
            //startListening()
            self.window!.orderOut(self)
        }
        else
        {
            self.window!.orderFront(self)
        }
        
        //self.window!.orderOut(self)
    }
    func startListening()
    {
        listen = NSSpeechRecognizer()
        var cmds = [name]
        listen.commands = cmds
        listen.listensInForegroundOnly = true
        //listen.blocksOtherRecognizers = true
        listen.delegate = self
        listen.startListening()
    }
    
//    func speechRecognizer(sender: NSSpeechRecognizer!, didRecognizeCommand command: AnyObject!) {
//        print("\(command as String) is talking to you \n")
//        statusBarItem.title = "Listen"
//    }
    
    @IBAction func buttonPressed(sender: NSButton) {
        //buttonPresses+=1
        //theLabel.stringValue = "Enter the closest English pronounciation of your name"
        //menuItem.title = "Clicked \(buttonPresses)"
        //listen.stopListening()
        name = nameText.stringValue
//        statusBarItem.title = "Listen"
        self.window!.orderOut(self)
        let read : String? = File.read("/path/to/file.txt")
        
        //println(read)
        
        let write : Bool = File.write("/path/to/file2.txt", content: "String to write")
        
        //println(write)
        
        
        
    }
    
    func setWindowVisible(sender: AnyObject){
        self.window!.orderFront(self)
    }
}
class File {
    
    class func exists (path: String) -> Bool {
        return NSFileManager().fileExistsAtPath(path)
    }
    
    class func read (path: String, encoding: NSStringEncoding = NSUTF8StringEncoding) -> String? {
        if File.exists(path) {
            return String.stringWithContentsOfFile(path, encoding: encoding, error: nil)!
        }
        
        return nil
    }
    
    class func write (path: String, content: String, encoding: NSStringEncoding = NSUTF8StringEncoding) -> Bool {
        return content.writeToFile(path, atomically: true, encoding: encoding, error: nil)
    }
}
