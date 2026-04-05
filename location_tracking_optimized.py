#!/usr/bin/env python
import sys
import os
import SiGploit
from subprocess import check_call, CalledProcessError

# Cache the current working directory
cwd = os.path.dirname(os.getcwd())

# Pre-compute all paths once
SS7_BASE = os.path.join(cwd, 'SS7/Tracking')
ATTACK_CONFIGS = {
    'sri': {'path': os.path.join(SS7_BASE, 'SRI'), 'jar': 'SendRoutingInfo.jar'},
    'srism': {'path': os.path.join(SS7_BASE, 'SRISM'), 'jar': 'SendRoutingInfoForSM.jar'},
    'psi': {'path': os.path.join(SS7_BASE, 'PSI'), 'jar': 'ProvideSubscriberInfo.jar'},
    'ati': {'path': os.path.join(SS7_BASE, 'ATI'), 'jar': 'AnyTimeInterrogation.jar'},
    'srigprs': {'path': os.path.join(SS7_BASE, 'SRIGPRS'), 'jar': 'SendRoutingInfoForGPRS.jar'},
}

def get_user_choice(prompt, options):
    """Helper function to get validated user input."""
    choice = raw_input(prompt).lower().strip()
    if choice in options.get('yes', ['y', 'yes']):
        return 'yes'
    elif choice in options.get('no', ['n', 'no']):
        return 'no'
    elif choice in options.get('exit', ['exit']):
        return 'exit'
    return None

def navigate_menus():
    """Handle menu navigation logic."""
    lt = get_user_choice('\nWould you like to go back to LocationTracking Menu? (y/n): ', 
                         {'yes': ['y', 'yes'], 'no': ['n', 'no']})
    if lt == 'yes':
        SiGploit.LocationTracking()
        return
    
    attack_menu = get_user_choice('Would you like to choose another attacks category? (y/n): ',
                                  {'yes': ['y', 'yes'], 'no': ['n', 'no']})
    if attack_menu == 'yes':
        SiGploit.attacksMenu()
        return
    
    main_menu = get_user_choice('Would you like to go back to the main menu? (y/exit): ',
                               {'yes': ['y', 'yes'], 'no': ['n', 'no'], 'exit': ['exit']})
    if main_menu == 'yes':
        SiGploit.mainMenu()
    elif main_menu == 'exit':
        print 'TCAP End...'
        sys.exit(0)

def run_attack(attack_name):
    """Generic function to run any attack by name."""
    if attack_name not in ATTACK_CONFIGS:
        print "\033[31mInvalid attack type: " + attack_name
        return
    
    config = ATTACK_CONFIGS[attack_name]
    jar_file = config['jar']
    jar_path = os.path.join(config['path'], jar_file)
    
    try:
        check_call(['java', '-jar', jar_path])
        navigate_menus()
    except CalledProcessError as e:
        print "\033[31m" + jar_file + " Failed to Launch, Error: " + str(e)

# Specific attack functions (thin wrappers for backward compatibility)
def sri():
    run_attack('sri')

def psi():
    run_attack('psi')

def srism():
    run_attack('srism')

def ati():
    run_attack('ati')

def srigprs():
    run_attack('srigprs')
