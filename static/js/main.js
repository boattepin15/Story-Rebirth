

const UpdateDay = () => {
    // Get Day locale thailand
    const today = new Date(Date().toLocaleString('th-TH', { timeZone: 'Asia/Bangkok' })).getDay()    
    const days = ['sunday','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
    const updateDayTabs = document.querySelectorAll('#updateDay #pills-tab-updateDay .nav-link');
    const tabContents = document.querySelectorAll('.tab-pane');
    
    // list class in tab and remove vale active
    updateDayTabs.forEach(tab => tab.classList.remove('active'));
    // list class in tab and remove vale show, active
    tabContents.forEach(tab => tab.classList.remove('show', 'active'));
    // qurey tab id from today
    const tabDayTab = document.querySelector(`#pills-${days[today]}-tab`);
    // qurey tab id from today
    const todayContent = document.querySelector(`#pills-${days[today]}`);
    
    // active and show content
    if (tabDayTab){
        tabDayTab?.classList.add('active');
        tabDayTab?.setAttribute("aria-selected", "true");
    }
    if (tabContents){
        todayContent?.classList.add('show', 'active');
    }
    

};


addEventListener('DOMContentLoaded', () => {
    UpdateDay()
});