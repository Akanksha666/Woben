from PIL import Image
import face_recognition
import cv2
import os
import sqlite3

# Get a reference to webcam #0 (the default one)
phone_number = input("Enter Emergency Phone Number : ")

video_capture = cv2.VideoCapture(0)

known_face_encodings=[]

known_face_names = []

user_appeared = []
root = "/Users/akanksha/hackathon/dataset/"

terrorlist_list = ['Akanksha', "Laden"]

for filename in os.listdir(root):
    if filename.endswith('.jpg' or '.png'):
        try:
            print(filename)
            path = os.path.join(root, filename)
            filter_image = face_recognition.load_image_file(path)
            filter_face_encoding = face_recognition.face_encodings(filter_image)
            known_face_encodings.append(filter_face_encoding[0])
            known_face_names.append(filename)
        except:
            print("An exception occurred : " + filename )

#print(known_face_encodings)
print(known_face_names)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
# process_this_frame = True

def face():

    while True:

        process_this_frame = True

        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                face_names.append(name.split('.jpg')[0][:-2])
        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            if name in terrorlist_list:
                # print("Terrorist Found with name : {}".format(name))
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                alert_string = "Terrorist Found - {}".format(name)
                cv2.putText(frame, alert_string,(10,500), font, 1,(255,255,255),2,cv2.LINE_AA)
                print("Emergency no : {}".format(phone_number))
                # terr_info = fetch_terr_info(name)
                # terr_location = get_terrorist_current_location()
                # mail_authorities(name, terr_location, terr_info)
                # send_sms_to_police(name, terr_location, terr_info)
                # call_police()

            else:
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 4), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

def mail_authorities(name, terr_location, terr_info):
    # import smtplib, ssl
    #
    # port = 587  # For starttls
    # smtp_server = "smtp.gmail.com"
    # sender_email = "amit88241123@gmail.com"
    # receiver_email = "sumit88241123@gmail.com"
    # password = "test123amit123"
    # message = """\
    # Subject: Hi there
    #
    # Found Terrorist- {}
    # at location - {}
    # having info - {}""".format(name, terr_location, terr_info)
    #
    # context = ssl.create_default_context()
    # with smtplib.SMTP(smtp_server, port) as server:
    #     server.ehlo()  # Can be omitted
    #     server.starttls(context=context)
    #     server.ehlo()  # Can be omitted
    #     server.login(sender_email, password)
    #     server.sendmail(sender_email, receiver_email, message)

    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    sender_email = ""  # Add sender's email
    receiver_email = ""  # Add reciever's email
    password = ""  # Add Password

    message = MIMEMultipart("alternative")
    message["Subject"] = "Terrorist Alert"
    message["From"] = sender_email
    message["To"] = receiver_email

    # transform_info = {"Name": terr_info[0],
    #                 "Country": terr_info[1],
    #                 "Age": terr_info[2],
    #                 "Attacks": terr_info[3],
    #                 "Last_Seen": terr_info[4]
    #                 "Crime_Expertised_in": terr_info[5],
    #                 }

    # Create the plain-text and HTML version of your message
    text = """\
    Found Terrorist- {}
    At location - {}
    Having info - {}""".format(name, terr_location, terr_info)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

def send_sms_to_police(name, terr_location, terr_info):
    from twilio.rest import Client

    account_sid = '' # Found on Twilio Console Dashboard
    auth_token = '' # Found on Twilio Console Dashboard

    myPhone = '+91{}'.format(phone_number) # Phone number you used to verify your Twilio account
    TwilioNumber = '+17868376523' # Phone number given to you by Twilio

    try:
        client = Client(account_sid, auth_token)
        client.messages.create(
        to=myPhone,
        from_=TwilioNumber,
        body= 'Terrorist {} Found at location {} ,having info - {}'.format(name, terr_location, terr_info) + u'\U0001f680')
    except Exception as e:
        raise e
    print("SMS sent to police")

def fetch_terr_info(name):
    info = []
    database = "test.sqlite3"
    # create a database connection
    conn = sqlite3.connect(database)
    print("Successfully estabilished db connection!")
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM data WHERE Name= '%s'" % name)
        rows = cur.fetchall()
        for row in rows:
            info.append(row)
            print(row)
    print("Fetched table data successfully")
    return info

def call_police():
    from twilio.rest import Client

    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)

    call = client.calls.create(
                            # url='https://drive.google.com/open?id=1n0Zmkub7oGHrCu5RcCPoi0kT3N4b5wMl',
                            url = 'http://demo.twilio.com/docs/voice.xml',
                            to='+91{}'.format(phone_number),
                            from_='+17868376523',
                        )

    print(call.sid)

def get_terrorist_current_location():
    import requests
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']  # ip_request.json() => {ip: 'XXX.XXX.XX.X'}
    print(my_ip)

    geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
    geo_request = requests.get(geo_request_url)
    geo_data = geo_request.json()
    print(geo_data)
    return geo_data

face()
