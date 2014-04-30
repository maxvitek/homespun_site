$(document).ready(function() {
    function getReply(url) {
        var request = new XMLHttpRequest();
            request.open('GET', url, false)
            request.send()
            return request.responseText;
        };

      var history = new Josh.History({ key: 'josh.homespun'});
      var shell = Josh.Shell({history: history});
      var promptCounter = 0;
      shell.onNewPrompt(function(callback) {
        callback("<span style='color: #a6bddb'>homespun</span><span style='color: #74c476'>$</span>");
      });
      
      shell.setCommandHandler("hue", {
        exec: function(cmd, args, callback) {
            var command = args[0] || '';
            var response = '';
            if(command === 'ls') {
                response = getReply('/hue/ls/');
            } else if(command === 'on') {
                var device = encodeURIComponent(args[1].split('_').join(' ')) || '';
                response = getReply('/hue/on/' + device)
            } else if(command === 'off') {
                var device = encodeURIComponent(args[1].split('_').join(' ')) || '';
                response = getReply('/hue/off/' + device)
            }
            callback(response)
        },
        completion: function(cmd, arg, line, callback) {
            callback(shell.bestMatch(arg, ['ls', 'on', 'off']))
        }
      });

      shell.setCommandHandler("wemo", {
        exec: function(cmd, args, callback) {
            var command = args[0] || '';
            var response = '';
            if(command === 'ls') {
                response = getReply('/wemo/ls/');
            } else if(command === 'on') {
                var device = encodeURIComponent(args[1].split('_').join(' ')) || '';    
                response = getReply('/wemo/on/' + device)
            } else if(command === 'off') {
                var device = encodeURIComponent(args[1].split('_').join(' ')) || '';
                response = getReply('/wemo/off/' + device)
            }
            callback(response)
        },
        completion: function(cmd, arg, line, callback) {
            callback(shell.bestMatch(arg, ['ls', 'on', 'off']))
        }
      });

      shell.setCommandHandler("nest", {
        exec: function(cmd, args, callback) {
            var command = args[0] || '';
            var response = '';
            if(command === 'set') {
                var temp = args[1] || '';
                response = getReply('/nest/set/' + temp);
            }
            callback(response)
        },
        completion: function(cmd, arg, line, callback) {
            callback(shell.bestMatch(arg, ['set']))
        }
      });

      
      shell.activate();
    });
