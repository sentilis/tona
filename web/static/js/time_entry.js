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
        var txtId = null;
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

        self.StartTimeEntry = function(start=Date.now()){
            btnStartTimeEntry = document.getElementById("start-time-entry");
            btnStopTimeEntry = document.getElementById("stop-time-entry");
            
            txtId = document.getElementById("time-entry-id");
            txtName = document.getElementById("time-entry-name");
            txtDuration = document.getElementById("time-entry-duration");
            
            if (btnStartTimeEntry != null){
                btnStartTimeEntry.classList.add('is-hidden');
            }
            if (btnStopTimeEntry != null){
                btnStopTimeEntry.classList.remove('is-hidden');
            }

            if ( typeof(start) === "string"){
                startTime = Date.parse(start+" UTC");
                self.Play();
                return;
            }
            startTime = start;
            startDateTime = new Date(startTime);
            
            fetch("/api/time-entry/start", {
                method: 'post',
                body: JSON.stringify({
                    "name": txtName.value,
                    "start": startDateTime.toISOString(),
                }),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            }).then(response => response.json()).then(function(data){
                self.Play()
                txtId.value = data['payload']['id'];
            }).catch(function(error){
                self.Stop()
                console.error(error);
            });
        };
        self.StopTimeEntry = function(){
            var stop = new Date();

            fetch("/api/time-entry/stop", {
                method: 'post',
                body: JSON.stringify({
                    "id": txtId.value,
                    "stop": stop.toISOString(),
                }),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            }).then(response => response.json()).then(function(data){
                self.Stop();
                txtId.value = "";
                if (btnStartTimeEntry != null){
                    btnStartTimeEntry.classList.remove('is-hidden');
                }
                if (btnStopTimeEntry != null){
                    btnStopTimeEntry.classList.add('is-hidden');
                }
            }).catch(function(error){
                console.error(error);
            });
        };

        return self;
    }   
    if (typeof(window.TonaTimeEntry) === 'undefined'){
        window.TonaTimeEntry = TonaTimeEntry();
    }
})(window);