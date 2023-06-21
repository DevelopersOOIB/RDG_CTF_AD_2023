import random
from requests import Session
from requests.auth import HTTPBasicAuth
from checklib import Status, generators
from random import shuffle

from src.parsing import HtmlParser
from src.models import NoteFilter, NoteSort

class CheckFabric:
    TCP_CONNECTION_TIMEOUT: int = 15
    CAT_RANDOM_PICTURE_URL: str = "https://thecatapi.com/api/images/get"

    def __init__(self, checker, port: int = 8080):
        self.checker = checker
        self.port = port
        self.base_url = f"http://{checker.host}:{port}"
        self.session = Session()

    def __make_details(self, status_code = None, *args) -> str:
        if status_code:
            return f"Code: {status_code}; Details: {list(args)}"
        return  f"Details: {list(args)}"

    def signup(self, username: str, password: str):
        url = f"{self.base_url}/users/signup"
        payload = {'username': username, 'password': password, 'repeatPassword': password}
        response = self.session.post(url, data=payload)
        
        if response.status_code == 200:
            parser = HtmlParser(response.text)
            if errors := parser.parse_register_error():
                self.checker.cquit(Status.MUMBLE, "Register failed", self.__make_details(errors))
            elif not parser.parse_register_success():
                self.checker.cquit(Status.MUMBLE, "Register failed",  self.__make_details("Not found success message"))
        else: 
            self.checker.cquit(Status.MUMBLE, "Register failed", self.__make_details(response.status_code, response.text))
    
    def signin(self, username: str, password: str):
        url = f"{self.base_url}/login"
        payload = {"username": username, "password": password}
        response = self.session.post(url, data=payload)
        
        if response.status_code == 200:
            parser = HtmlParser(response.text)
            if errors := parser.parse_login_error():
                self.checker.cquit(Status.MUMBLE, "Login failed", self.__make_details(errors))
            elif not parser.parse_login_success():
                self.checker.cquit(Status.MUMBLE, "Login failed", self.__make_details("Unable to get home page"))
        else: 
            self.checker.cquit(Status.MUMBLE, "Register failed", self.__make_details(response.status_code, response.text))
    
    def change_password(self, auth: HTTPBasicAuth, new_password: str):
        url = f"{self.base_url}/users/pwd-change"
        payload = {"oldPassword": auth.password, "newPassword": new_password} # type: ignore
        response = self.session.post(url, auth=auth, data=payload)
    
        if response.status_code == 200:
            parser = HtmlParser(response.text)
            if errors := parser.parse_change_password_error():
                self.checker.cquit(Status.MUMBLE, "Change password failed", self.__make_details(errors))
            elif not parser.parse_change_password_success():
                self.checker.cquit(Status.MUMBLE, "Change password failed", self.__make_details("Unable to get success message"))
            self.signin(auth.username, new_password)  # type: ignore
        else:
            self.checker.cquit(Status.MUMBLE, "Change password failed", self.__make_details(response.status_code, response.text))
        
    def actuator(self, auth: HTTPBasicAuth):
        url = f"{self.base_url}/actuator/health"
        response = self.session.get(url, auth=auth)

        if response.status_code == 200:
            data = response.json()
            if data and data['status'] != "UP":
                self.checker.cquit(Status.MUMBLE, "Actuator failed", self.__make_details("Could not get application status"))
        else:
            self.checker.cquit(Status.MUMBLE, "Actuator failed", self.__make_details(response.status_code, response.text))

    def link(self, auth: HTTPBasicAuth): 
        url = f"{self.base_url}/notes/check-link-availability"
        payload = {"link": self.CAT_RANDOM_PICTURE_URL}
        response = self.session.post(url, json=payload, auth=auth)
        
        if response.status_code == 200:
            data = response.json()
            if data and not data["success"]:
                self.checker.cquit(Status.MUMBLE, "Check link failed",  self.__make_details("The status for test link turned out to be FALSE"))
        else:
            self.checker.cquit(Status.MUMBLE, "Actuator failed", self.__make_details(response.status_code, response.text))
    
    def create_note(
        self, 
        auth: HTTPBasicAuth, 
        title: str = "test", 
        text_body: str = "test", 
        link: str = CAT_RANDOM_PICTURE_URL,
        isFlag = False
    ):
        url = f"{self.base_url}/notes"
        payload = {"title": title, "link": link,  "textBody": text_body}  
        response = self.session.post(url, data=payload, auth=auth)
        
        status = Status.CORRUPT if isFlag else Status.MUMBLE
        item = "Flag" if isFlag else "Note"
        if response.status_code == 200:
            parser = HtmlParser(response.text)
            note = parser.parse_last_note()
            if note:
                if note.get("title") != title:
                    self.checker.cquit(status, f"{item} creating failed", self.__make_details("Immutable titles for created and returned note"))
                if note.get("textBody") != text_body:
                    self.checker.cquit(status, f"{item} creating failed", self.__make_details("Immutable textBody for created and returned note"))
                return note.get("id")
            else:
                self.checker.cquit(status, f"{item} creating failed", self.__make_details("List of notes in response is empty"))
        else:
            self.checker.cquit(Status.MUMBLE, f"{item} creating failed", self.__make_details(response.status_code, response.text))
    
    def toogle_note_status(self, auth: HTTPBasicAuth, note_id):
        url = f"{self.base_url}/notes/{note_id}/toggle"
        response = self.session.patch(url, auth=auth)

        if response.status_code == 200:
            data = response.json()
            if data and not data.get('isCompleted'):
                self.checker.cquit(Status.MUMBLE, "Toogle note status failed", self.__make_details("Couldn't toogle note completion status"))
        else:
            self.checker.cquit(Status.MUMBLE, "Toogle note status failed", self.__make_details(response.status_code, response.text))

    def __add_test_note_and_toogle(self, auth: HTTPBasicAuth, total: int = 5, toggle: int = 3):
        url = f"{self.base_url}/notes"

        for i in range(total):
            self.create_note(auth, f'title-{i}', f'body-{i}')

        response = self.session.get(url, auth=auth)
        if response.status_code == 200:
            parser = HtmlParser(response.text)
            if notes := parser.parse_note_list()[:total]:
                random.shuffle(notes)
                for note in notes[:toggle]:
                    self.toogle_note_status(auth, note.get('id'))
            else:
                self.checker.cquit(Status.MUMBLE, "Note list filter failed", self.__make_details(f"Created {all} new notes, but response list is empty"))
        else:
            self.checker.cquit(Status.MUMBLE, "Note list filter failed", self.__make_details(response.status_code, response.text))

    def __check_filter(self, notes: list[dict], filter: NoteFilter):
        if filter == NoteFilter.ALL:
                return len(notes) > 0
        elif filter == NoteFilter.ACTIVE:
                return all(not note.get('isCompleted') for note in notes)
        elif filter == NoteFilter.COMPLETED:
                return all(note.get('isCompleted') for note in notes)
    
    def __is_filter_work(self, auth: HTTPBasicAuth, filter: NoteFilter):
        url = f"{self.base_url}/notes?filter={filter.value}"
        response = self.session.get(url, auth=auth)

        if response.status_code == 200:
            parser = HtmlParser(response.text)
            if notes := parser.parse_note_list():
                if not self.__check_filter(notes, filter):
                    self.checker.cquit(Status.MUMBLE, "Note list filter failed", self.__make_details(f"Filter not work for status: {filter}"))
            else:      
                self.checker.cquit(Status.MUMBLE, "Note list filter failed", self.__make_details(f"Returned todo list is empty"))
        else:
            self.checker.cquit(Status.MUMBLE, "Note list filter failed", self.__make_details(response.status_code, response.text))
                    
    def check_note_filter(self, auth: HTTPBasicAuth, total: int = 5, toggle: int = 3):
        self.__add_test_note_and_toogle(auth, total, toggle)
        self.__is_filter_work(auth, NoteFilter.ALL)
        self.__is_filter_work(auth, NoteFilter.ACTIVE)
        self.__is_filter_work(auth, NoteFilter.COMPLETED)
    
    def __is_sort_work(self, auth: HTTPBasicAuth, sort: NoteSort, count):
        filter = ""
        sortByField = ""
        if sort == NoteSort.TIMESTAMP:
                filter = NoteFilter.ALL
                sortByField = "createdAt" 
        elif sort == NoteSort.COMPLETED_AT:
                filter = NoteFilter.COMPLETED
                sortByField = "completedAt"

        url = f"{self.base_url}/notes?filter={filter.value}&sort={sort.value}"
        response = self.session.get(url, auth=auth)
        if response.status_code == 200:
            parser = HtmlParser(response.text)
            if notes := parser.parse_note_list()[:count]:
                notes_ = sorted(notes, key=lambda note: str(note.get(sortByField)), reverse=True)
                if notes != notes_:
                    self.checker.cquit(Status.MUMBLE, "Note list sort failed", self.__make_details(f"Filter not work for param: {filter}"))
            else:
                self.checker.cquit(Status.MUMBLE, "Note list sort failed", self.__make_details(f"Returned todo list is empty"))
        else:
            self.checker.cquit(Status.MUMBLE, "Note list sort failed", self.__make_details(response.status_code, response.text))
    
    def check_note_sort(self, auth: HTTPBasicAuth, total: int = 5, toggle: int = 3):
        self.__add_test_note_and_toogle(auth, total, toggle)
        self.__is_sort_work(auth, NoteSort.TIMESTAMP, total)
        self.__is_sort_work(auth, NoteSort.COMPLETED_AT, toggle)
    
    def create_flag(
        self, 
        auth: HTTPBasicAuth, 
        flag_id: str, 
        flag: str
    ): 
        return self.create_note(
            auth=auth, 
            title="Hey baby, maybe take a look inside",
            text_body=f"{flag_id} - {flag}",
            isFlag=True
        )

    def get_flag(
        self,
        auth: HTTPBasicAuth,
        flag_id: str,
        internal_flag_id: str,
        flag: str
    ):
        url = f"{self.base_url}/todo"
        response = self.session.get(url, auth=auth)
        textBody = f"{flag_id} - {flag}"

        if response.status_code == 200:
            parser = HtmlParser(response.text)
            notes = parser.parse_note_list()
            filters = filter(lambda note: note.get("id") == internal_flag_id, notes)
            if notes := list(filters):
                note_with_flag = notes[0]
                if note_with_flag.get("textBody") != textBody:  
                    self.checker.cquit(Status.CORRUPT, f"Flag getting failed", self.__make_details("Immutable textBody for puted and returned note"))
            else:
                self.checker.cquit(Status.CORRUPT, f"Flag getting failed", self.__make_details("Could not find flag at note list"))
        else:
            self.checker.cquit(Status.MUMBLE, f"Flag getting failed", self.__make_details(response.status_code, response.text))
