# OFFLINE MODE: Local Login Helper
# This module provides offline authentication without server checks
# It reads player account data from local files instead of connecting to server

from __future__ import absolute_import
from __future__ import print_function
import json
import os
import six.moves.builtins as builtins

OFFLINE_MODE = True
OFFLINE_ACCOUNTS_FILE = os.path.join(os.path.dirname(__file__), 'offline_accounts.json')
OFFLINE_PLAYERS_DIR = os.path.join(os.path.dirname(__file__), 'offline_players')

class OfflineLoginHelper:
    """Provides offline login functionality without server connection"""
    
    ACCOUNT_STATE_UNINITED = 0
    ACCOUNT_STATE_CONNECTING = 1
    ACCOUNT_STATE_INITTED = 2
    
    def __init__(self):
        self.account_data = None
        self.server_list = []
        self.registed_server_list = []
        self.account_state = self.ACCOUNT_STATE_UNINITED
        self.current_account = None
        self.current_password = None
        
    def load_offline_accounts(self):
        """Load account list from offline storage"""
        print('[OFFLINE] Loading accounts from local storage...')
        
        if not os.path.exists(OFFLINE_ACCOUNTS_FILE):
            print('[OFFLINE] Creating default accounts file...')
            self._create_default_accounts()
            
        try:
            with open(OFFLINE_ACCOUNTS_FILE, 'r') as f:
                accounts_data = json.load(f)
                return accounts_data.get('accounts', [])
        except Exception as e:
            print('[OFFLINE] Error loading accounts: %s' % str(e))
            return []
    
    def _create_default_accounts(self):
        """Create default offline accounts"""
        accounts = {
            'accounts': [
                {
                    'account': 'test',
                    'password': 'test',
                    'player_id': 'OFFLINE_PLAYER_001',
                    'player_name': 'Test Player',
                    'level': 50,
                    'exp': 10000
                },
                {
                    'account': 'admin',
                    'password': 'admin',
                    'player_id': 'OFFLINE_PLAYER_002',
                    'player_name': 'Admin',
                    'level': 100,
                    'exp': 999999
                }
            ]
        }
        
        os.makedirs(os.path.dirname(OFFLINE_ACCOUNTS_FILE), exist_ok=True)
        try:
            with open(OFFLINE_ACCOUNTS_FILE, 'w') as f:
                json.dump(accounts, f, indent=2)
            print('[OFFLINE] Default accounts created')
        except Exception as e:
            print('[OFFLINE] Error creating default accounts: %s' % str(e))
    
    def verify_login(self, account, password):
        """Verify account and password locally"""
        print('[OFFLINE] Verifying account offline: %s' % account)
        
        accounts = self.load_offline_accounts()
        
        for acc_data in accounts:
            if acc_data.get('account') == account and acc_data.get('password') == password:
                print('[OFFLINE] Account verified: %s' % account)
                self.current_account = account
                self.current_password = password
                self.account_data = acc_data
                self._set_global_player_data(acc_data)
                return True
        
        print('[OFFLINE] Account verification failed: %s' % account)
        return False
    
    def _set_global_player_data(self, player_data):
        """Set global player data for offline mode"""
        builtins.__dict__['PLAYER_ID'] = player_data.get('player_id', 'OFFLINE_PLAYER')
        builtins.__dict__['PLAYER_NAME'] = player_data.get('player_name', 'Offline Player')
        builtins.__dict__['PLAYER_LEVEL'] = player_data.get('level', 1)
        builtins.__dict__['OFFLINE_MODE'] = True
        builtins.__dict__['OFFLINE_ACCOUNT'] = player_data.get('account')
        
        print('[OFFLINE] Global player data set:')
        print('  PLAYER_ID: %s' % builtins.__dict__['PLAYER_ID'])
        print('  PLAYER_NAME: %s' % builtins.__dict__['PLAYER_NAME'])
        print('  PLAYER_LEVEL: %s' % builtins.__dict__['PLAYER_LEVEL'])
    
    def get_server_list(self):
        """Get default server list for offline mode"""
        print('[OFFLINE] Loading server list (offline mode)...')
        
        self.server_list = [
            {
                'svr_num': 1,
                'svr_name': 'LocalServer',
                'svr_ip': '127.0.0.1',
                'svr_port': 9000,
                'gate_ip': '127.0.0.1',
                'gate_port': 9001,
                'http_url': 'http://127.0.0.1:8080'
            }
        ]
        
        self.registed_server_list = self.server_list
        self.account_state = self.ACCOUNT_STATE_INITTED
        return self.server_list
    
    def connect_to_game_server(self, host_num):
        """Mock connection to game server - returns success immediately"""
        print('[OFFLINE] Connecting to offline game server (mock)...')
        return True
    
    def is_valid_session(self):
        """Check if current session is valid"""
        return self.current_account is not None
    
    def reset(self):
        """Reset login state"""
        self.current_account = None
        self.current_password = None
        self.account_data = None
        self.account_state = self.ACCOUNT_STATE_UNINITED


# Singleton instance
_offline_helper_instance = None

def get_offline_login_helper():
    """Get or create singleton instance"""
    global _offline_helper_instance
    if _offline_helper_instance is None:
        _offline_helper_instance = OfflineLoginHelper()
    return _offline_helper_instance
