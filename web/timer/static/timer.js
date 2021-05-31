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
    function TonaTimeEntry (){
        var self = {};
        
        var startTime = null;  // Date.now()
        var intervalId = null;  // setInterval()
        var txtName = null;
        var txtDuration = null; 
        var btnStartTimeEntry = null;
        var btnStopTimeEntry = null;

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
                if (txtDuration != null){                    
                    txtDuration.textContent = self.FormatDuration(seconds)
                }
            }, 1000);
        };

        self.Stop = function (){
            clearInterval(intervalId);
            startTime = null;
            intervalId = null; 
            txtDuration.textContent = "00:00:00"
        };

        self.ToggleButton = function(){
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

        self.StartTimeEntry = function(start=Date.now()){
            btnStartTimeEntry = document.getElementById("start-time-entry");
            btnStopTimeEntry = document.getElementById("stop-time-entry");
            
            txtName = document.getElementById("time-entry-name");
            txtDuration = document.getElementById("time-entry-duration");

            if ( typeof(start) === "string"){
                startTime = Date.parse(start+" UTC"); // TODO: after appened  UTC
                self.Play();
                self.ToggleButton()
                return;
            }
            startTime = start;
            startDateTime = new Date(startTime);
            self.request("start", {"name": txtName.value,"start": startDateTime.toISOString()})
        };

        self.StopTimeEntry = function(){
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
                if (action == "start"){
                    self.Play();
                    self.ToggleButton()
                }else if (action == "stop"){
                    self.Stop();
                    self.ToggleButton()
                    if (txtName !== null){
                        txtName.value = "";
                    }
                }
            }).catch(function(error){
                console.error(error);
            });
        };

        /**Widget TimeEntry */
        self.WidgetStartTimeEntry = function (event){
            var $timeEntry = event.target.parentNode.parentNode.parentNode;
            
            btnStartTimeEntry = $timeEntry.querySelector("a.start-time-entry");
            btnStopTimeEntry = $timeEntry.querySelector("a.stop-time-entry");
            txtDuration = $timeEntry.querySelector("span.time-entry-duration");
            startTime = Date.now();
            startDateTime = new Date(startTime);
            if (typeof($timeEntry.dataset.resModel)=== "string" && typeof($timeEntry.dataset.resId)=== "string"){
                var id = parseInt($timeEntry.dataset.resId);
                var model = $timeEntry.dataset.resModel;
                if (id>0 && model != "" ){
                    self.request("start", {res_id: id, res_model: model, "start": startDateTime.toISOString()})
                }
            }else if (typeof($timeEntry.dataset.name)=== "string"){
                var name = $timeEntry.dataset.name;
                if (name != "" ){
                    self.request("start", {name: name, "start": startDateTime.toISOString()})
                }
            }
        };
        
        return self;
    }
    
    if (typeof(window.TonaTimeEntry) === 'undefined'){
        window.TonaTimeEntry = TonaTimeEntry();
    }

})(window);

document.addEventListener("DOMContentLoaded", function(event) {
    
    (document.querySelectorAll('.widget-time-entry') || []).forEach(($timeEntry)=>{
        var start = $timeEntry.querySelector("a.start-time-entry");
        var stop = $timeEntry.querySelector("a.stop-time-entry");
        var duration = $timeEntry.querySelector("span.time-entry-duration");
        if (start === null || stop === null || duration === null){
            return;
        }
        start.addEventListener('click', self.TonaTimeEntry.WidgetStartTimeEntry);
        stop.addEventListener('click', self.TonaTimeEntry.StopTimeEntry);  
        
    });

    var timer_addons = document.querySelector("#timer-addons");
    if (timer_addons !== undefined){
        fetch("/api/time-entry/running", {
            method: 'get',
            headers: Tona.SetHeaders(),
        }).then(response => response.json()).then(function(data){
            if (data['ok']){
                var payload = data['payload']
                TonaTimeEntry.StartTimeEntry(payload['start']);
                var time_entry_name = timer_addons.querySelector("#time-entry-name")
                if ( time_entry_name !== undefined){
                    time_entry_name.value = payload['name'];
                }
            }
        }).catch(function(error){
            console.error(error);
        });
    }

});