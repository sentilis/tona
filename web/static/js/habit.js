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
    function Habit (){
        var self = {};
        
        self.API = "/api/habit";

        self.AddHabit = function (event){
            
            var modal = event.target.parentNode.parentNode;           
            var name = modal.querySelector("#habit-name");

            if (name.value != ""){
                var data = {name: name.value};
                fetch(self.API, {
                    method: 'post',
                    body: JSON.stringify(data),
                    headers: Tona.SetHeaders(),
                }).then(response => response.json()).then(function(data){
                    if (data['ok']){
                        var payload = data['payload'];
                        var menu = document.querySelector("#habit-menu-list");
                        var li = document.createElement("li");
                        li.innerHTML = '<a href="/habit/'+payload['id']+'">'+payload['name']+'</a>';
                        menu.append(li);
                        Tona.Modal.Close()
                        name.value = ""
                    }else{
                        console.warn(data)
                    }
                }).catch(function(error){
                    console.error(error);
                });
            }
        }; 

        self.AddCheckin = function(event, habit_id){
            var doc =  event.target.parentNode
            var id = "habit-checkin-name";
            var name = doc.querySelector("#"+id);
            var simplemde = Tona.QueueSimpleMDE[id]
            if ( Tona.IsSimpleMDE(simplemde) ){
                name.value = simplemde.value();
            }
            
            if (name.value != "") {

                var date = new Date()
                var data = {
                    name: name.value, 
                    checkin: date.getFullYear()+"-"+ (date.getMonth()+1) +"-"+ date.getDate(),
                    habit_id: habit_id
                }
                
                fetch( self.API+"/checkin", {
                    method: 'post',
                    body: JSON.stringify(data),
                    headers: Tona.SetHeaders(),
                }).then(response => response.json()).then(function(data){
                    if (data['ok']){
                        name.value = ""
                        if ( Tona.IsSimpleMDE(simplemde) ){
                            Tona.QueueSimpleMDE[id].value("");
                        }
                        Tona.Notification(event, "Your chekin is added", type="info", interval=1000)
                        self.LoadCheckin(event, habit_id);
                    }else{
                        Tona.Notification(event, data['message'])
                    }
                }).catch(function(error){
                    console.error(error);
                });
            }
        }

        self.LoadCheckin = function(event, habit_id, offset=1){
            var history = document.querySelector("#habit-checkin");
            if (offset == 1){
                history.innerHTML = "";
            }
            
            fetch(self.API +"/checkin?habit_id="+habit_id+"&offset="+offset+"&limit=10", {
                method: 'get',
                headers: Tona.SetHeaders(),
            }).then(response => response.json()).then(function(data){
                if (data['ok'] == true){
                    var payload = data['payload'];                    
                    
                    if (payload.length > 0){
                        for ( a = 0 ; a  < payload.length; a++ ){
                            var checkin = payload[a]
                            var msg = `<article class="media">
                                <div class="media-content">
                                <div class="content">
                                    <p>
                                    `+marked(checkin['name'])+`
                                    <small><a>`+checkin['checkin']+`</a></small>
                                    </p>
                                </div>
                                </div>
                            </article>`
                            history.innerHTML += msg
                        }
                        if (offset != 1){
                            history.querySelector("#checkin-show-more").remove()
                        }
                        history.innerHTML +=`<a onclick="Habit.LoadCheckin(`+null+`,`+habit_id+`,`+(offset+1)+`)" id="checkin-show-more">Show More</a>`
                    }else{
                        var sm = history.querySelector("#checkin-show-more");
                        if (sm != null){
                            sm.remove()
                            history.innerHTML +=`<a onclick="Habit.LoadCheckin(`+null+`,`+habit_id+`,`+1+`)" id="checkin-show-more">Show less</a>`
                        }
                    }   
                }
                
            }).catch(function(error){
                console.error(error);
            });

        };

        return self;
    }

    if (typeof(window.Habit) === 'undefined'){
        window.Habit = Habit();
    }

})(window);