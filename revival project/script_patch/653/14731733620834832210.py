# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/survey/ModeSatisfactionSurveyUI.py
from __future__ import absolute_import
import six
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CLOSE
from logic.gutils.new_template_utils import MultiChooseWidget
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from logic.gcommon.common_utils.local_text import get_text_by_id

class QuestionWidgetBase(object):

    def init_from_dict(self, ui_widget, question_idx, question_dict, answer_callback):
        self.question_idx = question_idx
        self.question_dict = question_dict
        self.required = question_dict.get('required', 0)
        self.title_text_id = question_dict.get('title_text_id', '')
        self.options = question_dict.get('options', [])
        self.type = question_dict.get('type', 'radio')
        self.ui_widget = ui_widget
        self.answer_callback = answer_callback
        self._sel_options = None
        self._recorded_size = None
        return

    def destroy(self):
        self.question_dict = {}
        self.answer_callback = None
        return

    def check_answer_callback(self, idx, is_sel):
        if self.answer_callback:
            self.answer_callback(self.question_idx, idx, is_sel)

    def init_question_widget(self, info_dict):
        pass

    def get_question_text(self):
        return get_text_by_id(self.title_text_id)

    def get_options_text(self):
        return [ get_text_by_id(opt.get('text_id', '')) for opt in self.options ]

    def set_vis(self, is_vis):
        if not self.ui_widget:
            return
        if not is_vis:
            if self.ui_widget.isVisible():
                self._recorded_size = self.ui_widget.getContentSize()
                self.ui_widget.SetContentSize(0, 0)
                self.ui_widget.setVisible(False)
        else:
            if self._recorded_size:
                self.ui_widget.setContentSize(self._recorded_size)
            self.ui_widget.setVisible(True)

    def is_answered(self):
        return False

    def get_selected_options(self):
        return None

    def get_selected_options_index(self):
        return None

    def get_question_result(self):
        result_dict = {}
        return result_dict

    def get_commit_result_text(self):
        result_dict = self.get_question_result()
        formatted_result = {}
        for question_name, answer_text in six.iteritems(result_dict):
            if answer_text is None:
                continue
            if type(answer_text) is list:
                formatted_result[question_name] = [ six.ensure_str(text) for text in answer_text if text ]
            else:
                formatted_result[question_name] = six.ensure_str(answer_text)

        return formatted_result


class SingleSelectionQuestion(QuestionWidgetBase):

    def init_question_widget(self, info_dict):
        self._init_single_select_question(self.ui_widget)

    def _init_single_select_question(self, ui_widget):
        container = ui_widget.comment_container
        question = self.question_dict
        ui_widget.lab_title1.SetString(question.get('title_text_id', ''))
        options = question.get('options', [])
        container.SetInitCount(len(options))
        all_item = container.GetAllItem()
        from logic.gutils.template_utils import init_radio_group_node_list
        init_radio_group_node_list(all_item)
        for idx, ui_item in enumerate(all_item):
            data = options[idx]
            ui_item.text.SetString(data.get('text_id', ''))

            @ui_item.unique_callback()
            def OnSelect(btn, choose, trigger_event, idx=idx):
                if choose:
                    self._sel_options = idx
                self.check_answer_callback(idx, choose)

        self.check_widget_size(ui_widget, container)

    def check_widget_size(self, ui_widget, container):
        old_size = ui_widget.getContentSize()
        container_size = container.GetContentSize()
        new_size = (old_size.width, old_size.height - container.getPosition().y + container_size[1])
        ui_widget.SetContentSize(*new_size)
        children = ui_widget.GetChildren()
        for child in children:
            if child != container:
                child.ResizeAndPosition()

        container.InitConfPosition()

    def get_selected_options_index(self):
        return self._sel_options

    def get_selected_options(self):
        if self._sel_options is not None:
            return self.options[self._sel_options]
        else:
            return {}
            return

    def is_answered(self):
        if not self.required:
            return True
        else:
            return self._sel_options is not None
            return None

    def get_question_result(self):
        res = self.get_selected_options().get('text_id')
        question_key = 'question_q%d' % (self.question_idx + 1)
        option_key = 'options_q%d' % (self.question_idx + 1)
        selected_keys = 'selected_q%d' % (self.question_idx + 1)
        result_dict = {question_key: self.get_question_text(),option_key: self.get_options_text(),
           selected_keys: get_text_by_id(res)
           }
        return result_dict


class MulSelectionQuestion(QuestionWidgetBase):

    def init_question_widget(self, info_dict):
        self._init_multiple_select_question(self.ui_widget)

    def _init_multiple_select_question(self, ui_widget):
        container = ui_widget.comment_container2
        question = self.question_dict
        show_reason_list = question.get('options', [])
        ui_widget.lab_title2.SetString(question.get('title_text_id', ''))
        container.SetInitCount(len(show_reason_list))
        all_item = container.GetAllItem()
        for idx, ui_item in enumerate(all_item):
            ui_item.text.SetString(show_reason_list[idx].get('text_id', ''))

        self.reasonMultiChooseWidget = MultiChooseWidget()
        self.reasonMultiChooseWidget.init(None, all_item, [])
        self.reasonMultiChooseWidget.SetCallbacks(self.OnSelItem, None)
        self.check_widget_size(ui_widget, container)
        return

    def check_widget_size(self, ui_widget, container):
        old_size = ui_widget.getContentSize()
        container_size = container.GetContentSize()
        new_size = (old_size.width, old_size.height - container.getPosition().y + container_size[1])
        ui_widget.SetContentSize(*new_size)
        children = ui_widget.GetChildren()
        for child in children:
            if child != container:
                child.ResizeAndPosition()

        container.InitConfPosition()

    def OnSelItem(self, idx, is_sel):
        self.check_answer_callback(idx, is_sel)

    def get_selected_options_index(self):
        if self.reasonMultiChooseWidget:
            return self.reasonMultiChooseWidget.GetSelects()
        else:
            return []

    def get_selected_options(self):
        sel_res = self.get_selected_options_index()
        res = []
        for sel in sel_res:
            opt = self.options[sel]
            res.append(opt)

        return res

    def is_answered(self):
        if not self.required:
            return True
        else:
            if self.get_selected_options_index():
                return True
            return False

    def get_question_result(self):
        sel_res = self.get_selected_options_index()
        res = []
        for sel in sel_res:
            opt = self.options[sel]
            res.append(get_text_by_id(opt.get('text_id', '')))

        question_key = 'question_q%d' % (self.question_idx + 1)
        option_key = 'options_q%d' % (self.question_idx + 1)
        selected_keys = 'selected_q%d' % (self.question_idx + 1)
        result_dict = {question_key: self.get_question_text(),option_key: self.get_options_text(),
           selected_keys: res
           }
        return result_dict


class BlankQuestion(QuestionWidgetBase):

    def init_question_widget(self, info_dict):
        self._init_input_box_question(self.ui_widget)
        if self._input_box:
            rise_panel = info_dict.get('rise_panel', None)
            if rise_panel:
                self._input_box.set_rise_widget(rise_panel)
        return

    def _init_input_box_question(self, ui_widget):
        import logic.comsys.common_ui.InputBox as InputBox
        question = self.question_dict
        ui_widget.lab_title3.SetString(question.get('title_text_id', ''))
        self._input_box = InputBox.InputBox(ui_widget.input_box, max_length=80)

    def get_selected_options_index(self):
        if self._input_box:
            return self._input_box.get_text()
        else:
            return ''

    def is_answered(self):
        if not self.required:
            return True
        else:
            if self._input_box.get_text():
                return True
            return False

    def get_selected_options(self):
        return self.get_selected_options_index()

    def get_question_result(self):
        question_key = 'question_q%d' % (self.question_idx + 1)
        ans_keys = 'text_q%d' % (self.question_idx + 1)
        result_dict = {question_key: self.get_question_text(),ans_keys: self.get_selected_options()
           }
        return result_dict


class SurveyQuestionWidget(object):

    def init_from_dict(self, question_idx, question_dict, answer_callback):
        self.question_idx = question_idx
        self.question_dict = question_dict
        self.type = question_dict.get('type', 'radio')
        self.init_question_template()
        self.ui_widget = None
        self.widget_class_inst = None
        self.answer_callback = answer_callback
        return

    def set_rise_panel(self, panel):
        self.rise_panel = panel

    def destroy(self):
        self.question_dict = {}
        self.rise_panel = None
        if self.widget_class_inst:
            self.widget_class_inst.destroy()
            self.widget_class_inst = None
        if self.ui_widget:
            self.ui_widget.release()
            self.ui_widget = None
        self.answer_callback = None
        return

    def init_question_template(self):
        self.QUESTION_TEMPLATE_DICT = {'radio': (
                   'comment/i_comment_1', SingleSelectionQuestion),
           'checkbox': (
                      'comment/i_comment_2', MulSelectionQuestion),
           'blank': (
                   'comment/i_comment_3', BlankQuestion)
           }

    def get_widget(self):
        return self.ui_widget

    def init_question_widget(self):
        if self.type not in self.QUESTION_TEMPLATE_DICT:
            raise ValueError('Unsupport question type!', self.type, self.QUESTION_TEMPLATE_DICT)
        template, widget_class = self.QUESTION_TEMPLATE_DICT[self.type]
        if not self.ui_widget:
            self.ui_widget = global_data.uisystem.load_template_create(template)
            self.ui_widget.retain()
        self.widget_class_inst = widget_class()
        self.widget_class_inst.init_from_dict(self.ui_widget, self.question_idx, self.question_dict, self.answer_callback)
        self.widget_class_inst.init_question_widget({'rise_panel': self.rise_panel})

    def check_answer_callback(self, idx, is_sel):
        if self.answer_callback:
            self.answer_callback(self.question_idx, idx, is_sel)

    def get_answer(self):
        return self.widget_class_inst.get_commit_result_text()

    def is_answered(self):
        return self.widget_class_inst.is_answered()

    def set_vis(self, is_vis):
        self.widget_class_inst.set_vis(is_vis)

    def get_selected_options(self):
        return self.widget_class_inst.get_selected_options()


class ModeSatisfactionSurveyUI(WindowMediumBase):
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    PANEL_CONFIG_NAME = 'comment/comment'
    TEMPLATE_NODE_NAME = 'report_window'
    UI_ACTION_EVENT = {'btn_confirm.btn_common.OnClick': 'on_confirm_report'
       }

    def on_init_panel(self, battle_context):
        super(ModeSatisfactionSurveyUI, self).on_init_panel()
        self._input_box = None
        self._cur_score = None
        survey_id = None
        all_survey = confmgr.get('custom_survey_config', 'SurveyConfig', 'Content', default={})
        for sur_id, survey_info in six.iteritems(all_survey):
            if survey_info.get('ui_class') == self.__class__.__name__:
                survey_id = sur_id

        self._survey_id = survey_id
        self._battle_context = battle_context
        self.init_ui()
        return

    def on_question_callback(self, question_idx, option_idx, is_sel):
        if question_idx < len(self.survey_widget_classes):
            survey_class = self.survey_widget_classes[question_idx]
            if question_idx == 0 and is_sel and survey_class.type == 'radio':
                option = survey_class.get_selected_options()
                if option.get('value', '') in ('SAT_DEGREE_BAD', 'SAT_DEGREE_VERY_BAD'):
                    self.set_reason_widget_visible(True)
                else:
                    self.set_reason_widget_visible(False)

    def init_ui(self):
        survey_conf = confmgr.get('custom_survey_config', 'SurveyConfig', 'Content', self._survey_id)
        questions = survey_conf['questions']
        self.survey_widget_classes = []
        for idx, qu in enumerate(questions):
            survey_widget = SurveyQuestionWidget()
            survey_widget.init_from_dict(idx, qu, self.on_question_callback)
            survey_widget.set_rise_panel(self.panel)
            survey_widget.init_question_widget()
            self.survey_widget_classes.append(survey_widget)

        self.panel.list_content.DeleteAllSubItem()
        for widget_class in self.survey_widget_classes:
            ui_widget = widget_class.get_widget()
            if ui_widget:
                self.panel.list_content.AddControl(ui_widget)

        self.set_reason_widget_visible(False)

    def set_reason_widget_visible(self, vis):
        self.REASON_WIDGET_INDEX = 1
        survey_class = self.survey_widget_classes[self.REASON_WIDGET_INDEX]
        if survey_class:
            survey_class.set_vis(vis)
        self.panel.list_content._container._refreshItemPos()
        self.panel.list_content._refreshItemPos()

    def on_finalize_panel(self):
        for survey_class in self.survey_widget_classes:
            if survey_class:
                survey_class.destroy()

        self.survey_widget_classes = []

    def on_click_close_btn(self, *args):
        self.close()

    def check_is_selection_valid(self):
        for survey_class in self.survey_widget_classes:
            if not survey_class.is_answered():
                return False

        return True

    def get_question_answers_dict(self):
        answer_dict = {'reward_type': '','reward_num': 0,'reward_trigger': 'no_reward'}
        for survey_class in self.survey_widget_classes:
            answer_dict.update(survey_class.get_answer())

        return answer_dict

    def on_confirm_report(self, btn, touch):
        if not self.check_is_selection_valid():
            global_data.game_mgr.show_tip(get_text_by_id(850021))
            return
        answer_dict = self.get_question_answers_dict()
        if global_data.player:
            global_data.player.commit_custom_survey(self._survey_id, answer_dict, self._battle_context)
            global_data.player.set_last_mode_sat_survey_record(self._battle_context)
        self.close()