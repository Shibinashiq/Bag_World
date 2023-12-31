let loc = window.location
let wsStart = loc.protocol ===  'ws://'
let endpoint = 'ws://127.0.0.1:8000/'
const USER_ID = $('#logged-in-user').val();
const recipient_user = $('#recipient-user-id').val();

let input_message = $('#input-message')
let message_body = $('.msg_card_body')
var socket = new WebSocket(endpoint);

function getCurrentTime() {
    const now = new Date();
    const date = now.toLocaleDateString();
    const time = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    return `${date}, ${time}`;
}

let message_element;  // Declare message_element outside the function

socket.onopen = async function (e) {
    $('#send-message-form').on('submit', function (e) {
        e.preventDefault();
        let message = input_message.val();
        let send_to;
        let thread_id = get_active_thread_id();

        if (USER_ID && recipient_user) {
            send_to = recipient_user
        } else {
            send_to = recipient_user
        }

        let data = {
            'message': message,
            'send_by': USER_ID,
            'send_to': send_to,
            'thread_id': thread_id
        }

        data = JSON.stringify(data);
        socket.send(data);
        $(this)[0].reset();
    });
}

socket.onmessage = async function (e) {
    let data = JSON.parse(e.data);
    let message = data['message']
    let send_by_id = data['send_by']
    newMessage(message, send_by_id)
}
socket.onerror = async function (e) {
    console.log('error', e)
}
socket.onclose = async function (e) {
    console.log('close', e)
}

function newMessage(message, send_by_id) {
    if ($.trim(message) === '') {
        return false;
    }

    if (send_by_id == USER_ID) {
        // Message sent by the user (align to the right)
        message_element = `
            <div class="d-flex mb-4 replied justify-content-start ">
                <div class="msg_cotainer_send alert alert-primary">
                    ${message} <br>
                    <span class="msg_time_send" style="font-size: 10px;">${getCurrentTime()}</span>
                </div>
            </div>
        `;
    } else {
        // Message received (align to the left)
        message_element = `
            <div class="d-flex mb-4 replied justify-content-end">
                <div class="msg_cotainer_admin alert alert-dark">
                    ${message} <br>
                    <span class="msg_time_send" style="font-size: 10px;">${getCurrentTime()}</span>
                </div>
            </div>
        `;
    }

    message_body.append($(message_element))
    message_body.animate({
        scrollTop: $(document).height()
    }, 100);
    input_message.val(null);
}

function get_active_thread_id() {
    let thread_id = $('.thread-id-input').val();
    if (!thread_id) {
        return null;
    }
    return thread_id;
}
