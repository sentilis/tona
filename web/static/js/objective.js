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
    function Objective (){
        var self = {};
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        };
        self.AddObjective = function (e){
            var $modal = document.querySelector("#modal-add-objective");
            var name = $modal.querySelector("#objetive-name");
            var start = $modal.querySelector("#objetive-start");
            var due = $modal.querySelector("#objetive-due");

            if (name.value != "" && start.value != "" && due.value != ""){
                var data = {name: name.value, start: start.value, due: due.value};
                fetch("/api/objective", {
                    method: 'post',
                    body: JSON.stringify(data),
                    headers: self.headers,
                }).then(response => response.json()).then(function(data){
                    console.log(data);
                    var menu = document.querySelector("#objective-menu-list");
                    var li = document.createElement("li");
                    var objective = data['payload'];
                    li.innerHTML = '<a href="/objective/'+objective['id']+'">'+objective['name']+'</a>';
                    menu.append(li);
                    Tona.Modal.Close()
                    name.value = ""
                    start.value = ""
                    due.value = ""
                }).catch(function(error){
                    console.error(error);
                });
                
            }            
        };

        self.AddKeyResult = function (e){
            var name = e.target;
            if (e.keyCode == 13 && name.value != "" ){
                var data = {
                    name: name.value, 
                    objective_id:  name.dataset.objectiveId,
                    start: name.dataset.objectiveStart,
                    due: name.dataset.objectiveDue
                }
                fetch("/api/objective/keyresult", {
                    method: 'post',
                    body: JSON.stringify(data),
                    headers: self.headers,
                }).then(response => response.json()).then(function(data){
                    console.log(data)
                    var menu = document.querySelector("#objective-key-menu-list");
                    var li = document.createElement("li");
                    var payload = data['payload'];
                    li.innerHTML = '<a href="/objective/'+payload['objective_id']['id']+'/keyresult/'+payload['id']+'">'+payload['name']+'</a>';
                    menu.append(li);
                    name.value = ""
                }).catch(function(error){
                    console.error(error);
                });
                
            }
        };

        self.EditKeyResult = function(e, id, field, value=null){
            var data = {};
            if (e != null && value == null){
                data[field]= e.target.value;
            }else if (e != null && value != null){
                data[field]= value;
            }
            fetch("/api/objective/keyresult/"+id, {
                method: 'put',
                body: JSON.stringify(data),
                headers: self.headers,
            }).then(response => response.json()).then(function(data){
                console.log(data)
            }).catch(function(error){
                console.error(error);
            });
        };

        self.AddCheckin = function(e, objective_keyresult_id){
            var comment = document.querySelector("#objective-keyreuslt-checkin-comment")
            if (comment.value != "") {
                var date = new Date()
                var data = {
                    name: comment.value, 
                    checkin: date.getFullYear()+"-"+ (date.getMonth()+1) +"-"+ date.getDate(),
                    objective_keyresult_id: objective_keyresult_id
                }
                
                fetch("/api/objective/keyresult/checkin", {
                    method: 'post',
                    body: JSON.stringify(data),
                    headers: self.headers,
                }).then(response => response.json()).then(function(data){
                    if (data['ok']){
                        comment.value = ""
                        Tona.Notification(e, "Your chekin is added", type="info")
                    }else{
                        Tona.Notification(e, data['message'])
                    }
                }).catch(function(error){
                    console.error(error);
                });
            }
        }

        self.LoadCheckin = function(e, objective_keyresult_id, offset=1){
            var history = document.querySelector("#objective-keyreuslt-history");
            if (offset == 1){
                history.innerHTML = "";
            }
            
            fetch("/api/objective/keyresult/checkin?objective_keyresult_id="+objective_keyresult_id+"&offset="+offset+"&limit=5", {
                method: 'get',
                headers: self.headers,
            }).then(response => response.json()).then(function(data){
                if (data['ok'] == true){
                    if (data['payload'].length > 0){
                        for ( a = 0 ; a  < data['payload'].length; a++ ){
                            var checkin = data['payload'][a]
                            var msg = `<article class="media">
                                <div class="media-content">
                                <div class="content">
                                    <p>
                                    <br>`+checkin['name']+`<br>
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
                        history.innerHTML +=`<a onclick="Objective.LoadCheckin(`+null+`,`+objective_keyresult_id+`,`+(offset+1)+`)" id="checkin-show-more">Show More</a>`
                    }else{
                        var sm = history.querySelector("#checkin-show-more");
                        if (sm != null){
                            sm.remove()
                            history.innerHTML +=`<a onclick="Objective.LoadCheckin(`+null+`,`+objective_keyresult_id+`,`+1+`)" id="checkin-show-more">Show less</a>`
                        }
                    }

                }

                
            }).catch(function(error){
                console.error(error);
            });

        };
        //https://medium.com/@guillaume.viguierjust/paging-sorting-filtering-and-retrieving-specific-fields-in-your-restful-api-a0d289bc574a
        return self;
    }
    if (typeof(window.Objective) === 'undefined'){
        window.Objective = Objective();
    }
})(window);


document.addEventListener("DOMContentLoaded", Tona.Tabs);