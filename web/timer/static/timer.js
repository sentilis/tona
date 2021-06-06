/*    Copyright (C) 2021  The Project TONA Authors
*
*    This program is free software: you can redistribute it and/or modify
*    it under the terms of the GNU General Public License as published by
*    the Free Software Foundation, either version 3 of the License, or
*    (at your option) any later version.
*
*    This program is distributed in the hope that it will be useful,
*    but WITHOUT ANY WARRANTY; without even the implied warranty of
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*    GNU General Public License for more details.
*
*    You should have received a copy of the GNU General Public License
*    along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

(function(window){
    function TimeEntry (){
        var self = {};
        
        var startTime = null;  // Date.now()
        var intervalId = null;  // setInterval()
        var txtName = null;
        var txtDuration = null;
        let menuDuration = null;


        self.FormatDuration = function (seconds, format="clock"){
            function pad(number) {
                var r = String(number);
                if ( r.length === 1 ) {
                  r = '0' + r;
                }
                return r;
              }
            var minutes = parseInt(seconds / 60);
            var hours  = parseInt(minutes / 60);
            seconds = parseInt(seconds - minutes * 60);
            minutes = parseInt(minutes - hours * 60);
            var d = pad(hours)+":"+pad(minutes)+":"+pad(seconds);
            if (format =="human") {
                d = pad(hours)+"H"+pad(minutes)+"M"+pad(seconds)+"S";
            }
            return d
        }

        self.Play = function (){
            intervalId = setInterval(function(){
                var delta = Date.now() - startTime;
                var seconds = Math.floor(delta/1000);  
                let duration = self.FormatDuration(seconds);
                if (txtDuration != null){                    
                    txtDuration.textContent = duration;
                }
                if (menuDuration != null){
                    if  (menuDuration.classList.contains('is-hidden')){
                        menuDuration.classList.remove('is-hidden')
                    }
                    menuDuration.textContent = duration;
                }
            }, 1000);
        };

        self.Stop = function (){
            clearInterval(intervalId);
            startTime = null;
            intervalId = null; 
            if (txtDuration !== null){
                txtDuration.textContent = "00:00:00"
            }
            if (menuDuration != null){
                if  (!menuDuration.classList.contains('is-hidden')){
                    menuDuration.classList.add('is-hidden')
                }
                menuDuration.textContent = "00:00:00";
            }
            if (txtName !== null){
                txtName.value = "";
            }
        };

        self.ToggleButton = function(){
            let btnStartTimeEntry = document.querySelector(".start-time-entry");
            let btnStopTimeEntry = document.querySelector(".stop-time-entry");

            if (btnStartTimeEntry != null && btnStopTimeEntry != null ){
                if (intervalId != null){
                    btnStartTimeEntry.classList.add('is-hidden');
                    btnStopTimeEntry.classList.remove('is-hidden');
                }else{
                    btnStartTimeEntry.classList.remove('is-hidden');
                    btnStopTimeEntry.classList.add('is-hidden');
                }
            }
        };

        self.StartTimeEntry = function(event, start=Date.now()){
            var widgetTimeEntry = event.target?.parentNode?.parentNode?.parentNode;
            let data = {};
            if (typeof(widgetTimeEntry?.dataset?.resModel)=== "string" && typeof(widgetTimeEntry?.dataset?.resId)=== "string"){
                data["res_id"] = parseInt(widgetTimeEntry.dataset.resId);
                data["res_model"] = widgetTimeEntry.dataset.resModel;
            }else if (typeof(widgetTimeEntry?.dataset?.name)=== "string"){
                data['name'] = timeEntry.dataset.name;
            }else if (document.getElementById("time-entry-name")){
                txtName = document.getElementById("time-entry-name");
                if (txtName !== null){
                    data['name'] = txtName.value;
                }                
            }          
            txtDuration = document.getElementById("time-entry-duration");
            menuDuration = document.querySelector("#menu-timer .time-entry-duration");

            if ( typeof(start) === "string"){
                startTime = Date.parse(start+" UTC"); // TODO: after appened  UTC
                self.Play();
                self.ToggleButton()
                return;
            }
            if ( (('res_id' in data) && ('res_model' in data)) || ('name' in data)){
                startTime = start;
                startDateTime = new Date(startTime);
                data['start'] = startDateTime.toISOString();
                self.request("start", data)
            }
        };

        self.StopTimeEntry = function(event){
            self.request("stop", null)
        };

        self.request = function(action, data){
            var url = "";
            if (action == "stop"){
                url = "/api/time-entry/stop";
                var stop = new Date();
                data = {"id": 0,"stop": stop.toISOString()}
            }else if (action == "start"){
                url = "/api/time-entry/start";
            }else {
                return;
            }
            fetch(url, {
                method: 'post',
                body: JSON.stringify(data),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            }).then(response => response.json()).then(function(data){
                if (data['ok']){
                    if (action == "start"){
                        self.Play();
                        self.ToggleButton()
                    }else if (action == "stop"){
                        self.Stop();
                        self.ToggleButton()
                    }
                }
              
            }).catch(function(error){
                console.error(error);
            });
        };
        
        self.Running = function(event){
            fetch("/api/time-entry/running", {
                method: 'get',
                headers: Tona.SetHeaders(),
            }).then(response => response.json()).then(function(data){
                if (data['ok']){
                    let payload = data['payload'];                    
                    let timer_menu = document.querySelector("#menu-timer");
                    if ( timer_menu !== null){
                        timer_menu.title = payload['name'];
                    }
                    let timer_addons = document.querySelector("#timer-addons");
                    if (timer_addons !== null){
                        var time_entry_name = timer_addons.querySelector("#time-entry-name");
                        if ( time_entry_name !== null){
                            time_entry_name.value = payload['name'];
                        }
                    }
                    self.StartTimeEntry(event, payload['start']);
                    self.ToggleButton();
                }
            }).catch(function(error){
                console.error(error);
            });
        };

        self.Widget = function (event){
            (document.querySelectorAll('.widget-time-entry') || []).forEach((widgetTimeEntry)=>{
                let content = `
                    <a onclick="TimeEntry.StartTimeEntry(event)" 
                        class="button is-small is-primary start-time-entry" title="Start time entry">
                        <span class="icon is-small">
                        <i class="fas fa-clock"></i>
                    </span>
                    </a>                  
                    <a onclick="TimeEntry.StopTimeEntry(event)" 
                        class="button is-small stop-time-entry is-hidden is-danger" title="Stop time entry">
                        <span class="icon">
                        <i class="fas fa-stop"></i>
                        </span>
                    </a>
                `;
                widgetTimeEntry.innerHTML = content;
                
            });
        };

        return self;
    }
    
    if (typeof(window.TimeEntry) === 'undefined'){
        window.TimeEntry = TimeEntry();
    }

})(window);

document.addEventListener("DOMContentLoaded", function(event) {
    TimeEntry.Widget(event);    
    TimeEntry.Running(event);

});