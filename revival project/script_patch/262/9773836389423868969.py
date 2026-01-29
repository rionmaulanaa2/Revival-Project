# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/SpringFestival/LuckyBagExpressAddressUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const import uiconst
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2, NormalConfirmUI2
from logic.comsys.common_ui import InputBox
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.cdata import adcode_data
from logic.gutils import template_utils

class LuckyBagExpressAddressUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202101/i_activity_lucky_bag_address'
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'close',
       'temp_confirm.btn_common.OnClick': 'on_confirm'
       }
    GLOBAL_EVENT = {'register_product_contact_succ': 'register_finish'
       }

    def on_init_panel(self, *args, **kwargs):
        self.item_no = None
        self.init_parameters()
        self.init_input_boxes()
        self.init_province_choose_list()
        self.reset_city_choose_list()
        self.reset_district_choose_list()
        return

    def set_use_params(self, item_data, *args, **kwargs):
        item_no = item_data.get('item_no', None)
        self.item_no = item_no
        if item_no is None:
            self.close()
            return
        else:
            player = global_data.player
            item = player.get_item_by_no(item_no)
            if not item.can_use(player.get_sex(), player.get_lv()):
                self.hide()
                NormalConfirmUI2(content='\xe4\xbd\xa0\xe5\xb7\xb2\xe7\xbb\x8f\xe5\xa1\xab\xe5\x86\x99\xe8\xbf\x87\xe6\x94\xb6\xe4\xbb\xb6\xe5\x9c\xb0\xe5\x9d\x80\xe4\xba\x86\xef\xbc\x8c\xe8\xaf\xb7\xe8\x80\x90\xe5\xbf\x83\xe7\xad\x89\xe5\xbe\x85\xe5\x8f\x91\xe8\xb4\xa7\xe5\x90\xa7!', on_confirm=lambda : self.close())
                return
            return

    def init_parameters(self):
        self.province_adcode = None
        self.city_adcode = None
        self.district_adcode = None
        return

    def init_input_boxes(self):
        self.name_box = InputBox.InputBox(self.panel.input_box_name, placeholder=get_text_by_id(601130))
        self.phone_box = InputBox.InputBox(self.panel.input_box_phone, placeholder=get_text_by_id(601148))
        self.address_box = InputBox.InputBox(self.panel.input_box_address, placeholder=get_text_by_id(601137))
        self.name_box.set_rise_widget(self.panel)
        self.phone_box.set_rise_widget(self.panel)
        self.address_box.set_rise_widget(self.panel)

    def init_province_choose_list(self):
        province_list = self._get_province_list()
        self.panel.lab_nation_01.SetString(601133)

        @self.panel.btn_location_01.unique_callback()
        def OnClick(*args):
            self.panel.province_list.setVisible(True)
            self.panel.img_click_01.setRotation(180)

        def choose(index):
            selected = province_list[index]
            province_name = selected['name']
            self.province_adcode = selected['adcode']
            self.panel.lab_nation_01.SetString(province_name)
            self.reset_district_choose_list()
            self.init_city_choose_list()

        template_utils.init_common_choose_list_2(self.panel.province_list, self.panel.img_click_01, province_list, callback=choose, max_height=200)

    def init_city_choose_list(self):
        if not self.province_adcode:
            return
        city_list = self._get_city_list()
        self.panel.btn_location_02.setVisible(True)
        self.panel.btn_location_02.SetEnable(True)
        self.panel.lab_nation_02.SetString(601134)

        @self.panel.btn_location_02.unique_callback()
        def OnClick(*args):
            self.panel.city_list.setVisible(True)
            self.panel.img_click_02.setRotation(180)

        def choose(index):
            selected = city_list[index]
            city_name = selected['name']
            self.city_adcode = selected['adcode']
            self.panel.lab_nation_02.SetString(city_name)
            self.init_district_choose_list()

        template_utils.init_common_choose_list_2(self.panel.city_list, self.panel.img_click_02, city_list, callback=choose, max_height=200)
        if adcode_data.is_municipality(self.province_adcode):
            choose(0)

    def reset_city_choose_list(self):
        self.panel.btn_location_02.setVisible(False)
        self.panel.btn_location_02.SetEnable(False)
        self.panel.lab_nation_02.SetString(601134)

    def init_district_choose_list(self):
        if not self.province_adcode or not self.city_adcode:
            return
        district_list = self._get_district_list()
        self.panel.btn_location_03.setVisible(True)
        self.panel.btn_location_03.SetEnable(True)
        self.panel.lab_nation_03.SetString(601135)

        @self.panel.btn_location_03.unique_callback()
        def OnClick(*args):
            self.panel.town_list.setVisible(True)
            self.panel.img_click_03.setRotation(180)

        def choose(index):
            selected = district_list[index]
            city_name = selected['name']
            self.district_adcode = selected['adcode']
            self.panel.lab_nation_03.SetString(city_name)

        template_utils.init_common_choose_list_2(self.panel.town_list, self.panel.img_click_03, district_list, callback=choose, max_height=200)

    def reset_district_choose_list(self):
        self.panel.btn_location_03.setVisible(False)
        self.panel.btn_location_03.SetEnable(False)
        self.panel.lab_nation_03.SetString(601135)

    def _get_province_list(self):
        EXCEPT_PROVINCE_CODE = ('71', '81', '82')
        province_list = []
        for prov in sorted(adcode_data.provinces_set):
            if prov in EXCEPT_PROVINCE_CODE:
                continue
            province_code = '{}0000'.format(prov)
            if adcode_data.is_adcode_valid(province_code):
                province_list.append({'name': adcode_data.data[province_code],
                   'adcode': province_code
                   })

        return province_list

    def _get_city_list(self):
        city_adcode_list = adcode_data.get_city_list_by_province(self.province_adcode)
        return [ {'name': adcode_data.data[city_code],'adcode': city_code} for city_code in city_adcode_list
               ]

    def _get_district_list(self):
        district_adcode_list = adcode_data.get_district_list_by_city(self.city_adcode)
        return [ {'name': adcode_data.data[district_code],'adcode': district_code} for district_code in district_adcode_list
               ]

    def on_confirm(self, *args):
        name = self.name_box.get_text()
        phone = self.phone_box.get_text()
        address_details = self.address_box.get_text()
        province = self.panel.lab_nation_01.getString()
        city = self.panel.lab_nation_02.getString()
        district = self.panel.lab_nation_03.getString()
        if not name:
            NormalConfirmUI2(content=get_text_by_id(601130))
            return
        if not phone:
            NormalConfirmUI2(content=get_text_by_id(601148))
            return
        if not self.province_adcode:
            NormalConfirmUI2(content=get_text_by_id(601183))
            return
        if not address_details:
            NormalConfirmUI2(content=get_text_by_id(601137))
            return
        confirm_txt = get_text_by_id(601169, args={'name': name,
           'phone': phone,
           'province': province,
           'city': city,
           'district': district,
           'details': address_details
           })

        def upload_express_data():
            player = global_data.player
            item = player.get_item_by_no(self.item_no)
            item_num = player.get_item_num_by_no(self.item_no)
            if item_num < 0:
                return
            player.use_item(item.id, 1, {'contact': (name, phone, province, city, district, address_details)})

        second_confirm_ui = SecondConfirmDlg2()
        second_confirm_ui.confirm(content=confirm_txt, confirm_callback=upload_express_data)

    def register_finish(self, item_no):
        if str(item_no) == str(self.item_no):
            global_data.game_mgr.show_tip(931037)
            self.close()