function sendAjax(data) {
  data = JSON.stringify(data);
  console.log(data);
  addSpinner();
  $.ajax({
    sync: 'true',
    type: 'POST',
    url: '/webcrawler',
    data: data,
    success: function(message) {
      if (message.message == 'success') {
        console.log(message.message)
      }
      else {
        alert(message.message)
      };
    },
    error: function(xhr, status) {
      alert('Status', status, 'Error:', xhr)
    }
  });
  removeSpinner()
}

function openChrome() {
  data = {
    'message': 'open'
  };
  sendAjax(data);
  $('#btnType').attr('onClick', 'typeUserAndPass()').removeClass('btn-wait');
  $('#btnVisit').attr('onClick', 'visitCompany()').removeClass('btn-wait');
}

function typeUserAndPass() {
  data = {
    'message': 'type',
    'username': $('#username').val(),
    'password': $('#password').val()
  };
  sendAjax(data)
}

function visitCompany() {
  data = {
    'message': 'visit',
    'url': 'https://www.linkedin.com/company/'+$('#url').val()
  };
  sendAjax(data)
  $('#btnCrawl').attr('onClick','startCrawling()').removeClass('btn-wait');
}

function startCrawling() {
  data = {
    'message': 'start',
  };
  sendAjax(data)
}

function addSpinner() {
  let width =  String(window.innerWidth/2)
  let height = String(window.innerHeight/4)
  let ele = `
  <div id="spinner" class="modal-backdrop fade show">
    <div class="d-flex justify-content-center">
      <div class="spinner-border" style="width:`  + width +
      `px; height:` + width + `px; margin-top:` + height + `px" role="status"></div>
    </div>
  </div>`;
  $('body').prepend(ele);
}

function removeSpinner() {
  $('#spinner').remove()
}
