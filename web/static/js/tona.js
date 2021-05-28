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
if ( !Date.prototype.toISOString ) {
    ( function() {
  
        function pad(number) {
          var r = String(number);
          if ( r.length === 1 ) {
            r = '0' + r;
          }
          return r;
        }
    
        Date.prototype.toISOString = function() {
          return this.getUTCFullYear()
            + '-' + pad( this.getUTCMonth() + 1 )
            + '-' + pad( this.getUTCDate() )
            + 'T' + pad( this.getUTCHours() )
            + ':' + pad( this.getUTCMinutes() )
            + ':' + pad( this.getUTCSeconds() )
            + '.' + String( (this.getUTCMilliseconds()/1000).toFixed(3) ).slice( 2, 5 )
            + 'Z';
        };
    
      }() );
}

(function(window){
  function Tona (){
      var self = {};

      self.URLQuery = function(params){
        const esc = encodeURIComponent;
        var query = ""
        for (const param in params){
          if (params[param]){
            query += `${esc(param)}=${esc(params[param])}&`
          }
        } 
        return query
      }

      self.Notification = function(e, msg=null, type="danger", interval=5000){
        classColor = "is-danger"
        switch(type){
          case "info":
            classColor = "is-info"
            break;
          case "success":
            classColor = "is-success"
            break;
          case "warning":
              classColor = "is-warning"
              break;
          case "danger":
          default:
        }
        (document.querySelectorAll('.notification') || []).forEach(($node) => {
          var $notification = $node.parentNode;
          $notification.classList.remove('is-hidden');
          $node.classList.add(classColor);
          if (msg != null){
            $node.querySelector("#notification-content").innerHTML = msg
          }
          var $delete = $notification.querySelector(".delete");
          if ($delete != null){
            $delete.addEventListener('click', () => {
              $notification.classList.add("is-hidden");
              $node.classList.remove(classColor);
            });
            setInterval(function() {
              $notification.classList.add("is-hidden");
              $node.classList.remove(classColor);
            }, interval);
          }
        });
      }

      self.Modal = {
        modal : null,
        Close: function (){
          self.Modal.modal.classList.remove('is-active');
          self.Modal.modal = null;
        },
        Show : function(id){
          self.Modal.modal = document.getElementById(id);
          self.Modal.modal.classList.add('is-active');
          
          (self.Modal.modal.querySelectorAll('.modal-card-head .delete') || []).forEach(($delete)=>{
            $delete.addEventListener('click', self.Modal.Close);
          });
          
          (self.Modal.modal.querySelectorAll('.modal-card-foot button:not(.is-success)') || []).forEach(($delete)=>{
            $delete.addEventListener('click', self.Modal.Close);
          });
        },

      };
      
      self.Tabs = function(){
        (document.querySelectorAll('.tabs') || []).forEach(($tabs)=>{
          ($tabs.querySelectorAll('a') || []).forEach(($a)=>{
              $a.addEventListener('click', (e)=>{
                  $ul = e.target.parentNode.parentNode;
                  var tabsGroup = $ul.dataset.tabsGroup;
                  var tabId = e.target.dataset.tabId;
                  $li = $ul.querySelector("li.is-active");
                  if ($li.classList != null){
                      $li.classList.remove('is-active')
                  }
                  if (e.target.parentNode.classList != null){
                      e.target.parentNode.classList.add('is-active')
                  }
                  (document.querySelectorAll("[data-tabs-group-id='"+tabsGroup+"']") || []).forEach(($tabContent)=>{
                    if ($tabContent.id == tabsGroup+"-"+tabId){
                      $tabContent.classList.remove("is-hidden");
                    }else{
                      $tabContent.classList.add("is-hidden");
                    }
                  });
              }); 
          });        
        });
      };

      self.SetHeaders = function(headers={}) {
        
        var dafaultHeaders = {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }

        if(localStorage.jwt) {
          dafaultHeaders['Authorization'] = `Bearer ${localStorage.jwt}`;
        } 
        
        return {
          ...headers,
          ...dafaultHeaders
        }

      };

      self.IsSimpleMDE = function (o){
        if (o.toTextArea !== undefined  & o.isPreviewActive !== undefined ){
          return true;
        }
        return false;
      }
      
      self.QueueSimpleMDE = {};

      self.SimpleMDE = function(){
        /**
         * Apply elements with class .textarea-markdown, markdown editor
         */
        document.addEventListener("DOMContentLoaded", function(event) {
          (document.querySelectorAll('.textarea-markdown') || []).forEach(($md)=>{
              var simplemde = new SimpleMDE({ element: $md, forceSync: true, tabSize: 1});
              if ($md.onblur !== null ){            
                  simplemde.codemirror.on("blur", function(event){
                      $md.onblur(simplemde)            
                  });
              }
              if ($md !== ''){
                self.QueueSimpleMDE[$md.id] = simplemde;
              }
          });
        });
      }

      self.Dropdown = function (){
        document.addEventListener("DOMContentLoaded", function(event) {
          (document.querySelectorAll('.dropdown') || []).forEach((dropdown)=>{
            dropdown.addEventListener('click', (e)=>{
              var isActive = false;
              if (dropdown.classList && dropdown.classList.length > 0){
                  for (var a = 0  ;  a < dropdown.classList.length; a++){
                      if (dropdown.classList[a] == 'is-active'){
                          isActive = true;
                      }
                  }
              }
              if (isActive){
                  dropdown.classList.remove("is-active");
              }else{
                dropdown.classList.add("is-active");
              }
            });
          }); 
        });
      }
      return self;
  }

  if (typeof(window.Tona) === 'undefined'){
    window.Tona = Tona();
  }
})(window);

/** Auto apply styles | accions */
( function() {
  Tona.Dropdown();
}() );