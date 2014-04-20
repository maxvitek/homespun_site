$(document).ready(function() {
      var history = new Josh.History({ key: 'josh.homespun'});
      var shell = Josh.Shell({history: history});
      var promptCounter = 0;
      shell.onNewPrompt(function(callback) {
        callback("<span style='color: #a6bddb'>homespun</span><span style='color: #74c476'>$</span>");
      });
      shell.setCommandHandler("hello", {
        exec: function(cmd, args, callback) {
          var arg = args[0] || '';
          var response = "who is this " + arg + " you are talking to?";
          if(arg === 'josh') {
            response = 'pleased to meet you.';
          } else if(arg === 'world') {
            response = 'world says hi.'
          } else if(!arg) {
            response = 'who are you saying hello to?';
          }
          callback(response);
        },
        completion: function(cmd, arg, line, callback) {
          callback(shell.bestMatch(arg, ['world', 'josh']))
        }
      });
      shell.activate();
    });
