import kivy
from kivy.uix.floatlayout import FloatLayout 
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.button import Button 
from kivy.uix.label import Label 
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.uix.popup import Popup 
from source import Controller
import matplotlib.pyplot as plt 
from functools import partial

acc = None

class CreateWindow(Screen):
    pass
class HomeWindow(Screen):
    pass
class BrowseWindow(Screen):
    def upload(self, file_name):
        addr = file_name[0]
        LoadingWindow.src =  addr
        sm.current = "load"
class LoadingWindow(Screen):
    src = ""
    def on_enter(self, *args):
        global acc
        acc = Controller.Account(self.src)
        sm.current = "port"
class PortWindow(Screen):
    tval = ObjectProperty(None)
    growth = ObjectProperty(None)
    n_asst = ObjectProperty(None)
    m_sip = ObjectProperty(None)
    fig = ObjectProperty(None)
    def on_enter(self, *args):
        global acc
        self.n_asst.text = "Total_number of Assets : "+str(len(acc.pf.asset_list))
        self.tval.text = "Total Value = "+str(acc.pf.t_val)
        self.growth.text = "Overall Growth : {:.2f}%".format(acc.pf.t_int*100/acc.pf.t_inv)
        self.m_sip.text = "Monthly SIP amount : "+str(acc.pf.m_sip)
        self.plot_bar()
        self.fig.source = './source/fig.png'
    def plot_bar(self):
        global acc
        fig= plt.figure(figsize=(6,3))
        ax = plt.subplot('111')
        ax.axes.set_xlim(-.5,2)
        plt.bar(['Invested','Interest'],[acc.pf.t_inv, acc.pf.t_int], color=['blue','green'], width=0.4,)
        labels = [acc.pf.t_inv,acc.pf.t_int]
        handles = [plt.Rectangle((0,0),1,1, color=i) for i in ['blue','green']]
        plt.legend(handles,labels)
        plt.savefig('./source/fig.png')
        plt.close()
class AllocationWindow(Screen):
    tval = ObjectProperty(None)
    pie = ObjectProperty(None)
    def on_enter(self, *args):
        global acc
        self.tval.text = f"Total Value \n   {acc.pf.t_val}"
        self.plot_pie()
        self.pie.source = './source/pie.png'
    def plot_pie(self):
        global acc
        tot = sum(acc.pf.allo.values())
        patches, texts = plt.pie(acc.pf.allo.values())
        labels = [f"{i}  {acc.pf.allo[i]*100/tot:.1f}%" for i in acc.pf.allo.keys()]
        plt.legend(patches, labels, loc='center left', bbox_to_anchor=(-0.1, 1.), fontsize=10)
        plt.savefig('./source/pie.png')

class AssetWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def back_btn(self, instance):
        port.root.current = 'port'
        port.root.transition.direction='right'
    first = "True"
    def create_page(self):
        global acc
        head = FloatLayout()
        self.header = Label(text='Name      Type      XIRR', size_hint_y=0.07, pos_hint={"x":0.0,"top":1})
        head.add_widget(self.header)
        self.back = Button(text='Back', pos_hint={"x":0.02,"top":0.98},size_hint=(0.05,0.05))
        self.back.bind(on_press=self.back_btn)
        head.add_widget(self.back)
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        num = len(acc.pf.asset_list)
        i=1
        for asset in acc.pf.asset_list:
            self.join = Button(text=f'{i}.  {asset.a_name}     {asset.a_type}     {asset.int_rate*100:.2f}%',size_hint_y=None, height=50 )
            self.join.bind(on_press=partial(self.create_popup, asset))
            layout.add_widget(self.join)
            i+=1
        
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height-50))
        root.add_widget(layout)
        page = FloatLayout()
        head.add_widget(root)
        self.add_widget(head)
        
    def create_popup(self, asset, *args):
        self.plot_bar(asset)
        show = PopupWindow()
        show.nme.text = asset.a_name
        show.typ.text = f"Type: {asset.a_type}"
        show.amt.text = f"Invested: {asset.inv_amt} Rs."
        show.dte.text = f"Time Invested: {asset.time_inv[2]} years {asset.time_inv[1]} months {asset.time_inv[0]} days"
        show.intr.text = f"Interest Rate: {asset.int_rate*100:.2f}%"
        
        show.bar.source = './source/bar.png'
        show.bar.reload()
        popWind = Popup(title="Asset Performance", content = show,
                        size_hint=(None, None), size = (600,500))
        popWind.open()
        show.close.bind(on_press = popWind.dismiss)
    def plot_bar(self,asset):
        fig= plt.figure(figsize=(6,3))
        ax = plt.subplot('111')
        ax.axes.set_xlim(-.5,2)
        plt.bar(['Invested','Interest'],[asset.inv_amt, asset.get_int_amt()],color=['blue','green'], width=0.4,)
        labels = [asset.inv_amt,asset.get_int_amt()]
        handles = [plt.Rectangle((0,0),1,1, color=i) for i in ['blue','green']]
        plt.legend(handles,labels)
        plt.savefig('./source/bar.png')
        plt.close()
    def on_enter(self, *args):
        if self.first=="True":
            self.create_page()
        self.first="False"
class PopupWindow(FloatLayout):
    nme = ObjectProperty(None)
    close = ObjectProperty(None)
    typ = ObjectProperty(None)
    amt = ObjectProperty(None)
    dte = ObjectProperty(None)
    intr = ObjectProperty(None)
    bar = ObjectProperty(None)

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("./source/portman.kv")

sm = WindowManager()
screens = [HomeWindow(name="home"), BrowseWindow(name="browse"),PortWindow(name="port"),
 CreateWindow(name="create"), LoadingWindow(name="load"), AllocationWindow(name="alloc"),
 AssetWindow(name="assets")]
for screen in screens:
    sm.add_widget(screen)
sm.current = "home"
class PortMan(App):
    def build(self):
        return sm

if __name__ == "__main__":
    port = PortMan()
    port.run()