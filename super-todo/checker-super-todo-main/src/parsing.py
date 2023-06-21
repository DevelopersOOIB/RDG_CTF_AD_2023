from bs4 import BeautifulSoup, Tag

class HtmlParser:
    def __init__(self, html: str):
        self.soap = BeautifulSoup(html,  'html.parser')

    def parse_register_error(self) -> list[str]:
        errors = []
        if pills := self.soap.find("div", id="pills-register"):
            containers = pills.find_all("div", class_="form-floating") # type: ignore
            for container in containers:
                if error := container.find("p"):
                    errors.append(error.text.strip())
        return errors
    
    def parse_login_error(self) -> list[str]:
        errors = []
        if pills := self.soap.find("div", id="pills-login"):
            containers = pills.find_all("div", class_="alert-danger") # type: ignore
            for container in containers:
                errors.append(container.text.strip())
        return errors
    
    def parse_change_password_error(self) -> list[str]:
        errors = []
        if divs := self.soap.find_all("div", class_="form-floating"):
            for div in divs:
                if error := div.find("div", class_="alert-danger"): # type: ignore
                    words = (error.text
                        .replace('\r\n', '')
                        .replace('\n', '')
                        .split(" "))
                    errors.append(" ".join(filter(None, words)))
        return errors

    def parse_register_success(self) -> bool:
        
        if container := self.soap.find("div", id="customxV"):
            if "Account has been created" in container.text:
                return True
        return False
    
    def parse_login_success(self) -> bool:
        if self.soap.find("div", id="content"):
            return True
        return False
    
    def parse_change_password_success(self) -> bool:
        if self.soap.find("div",  class_="alert-success"):
            return True
        return False
    
    def parse_last_note(self):
        if container := self.soap.find("div", id="note-list"):
            note = container.find_all("ul")[-1] # type: ignore
            return self.parse_note(note)
    
    def parse_note_list(self) -> list[dict[str, str]]:
        result = []
        if container := self.soap.find("div", id="note-list"):
            notes = container.find_all("ul") # type: ignore
            for note in notes:
                payload = self.parse_note(note)
                result.append(payload)               
        return result[::-1]
    
    def parse_note(self, note: Tag):
        payload = {}
        if id := note.get("id"):
            payload["id"] = id
        if createdAt := note.get("created-at"):
            payload['createdAt'] = createdAt
        if completedAt := note.get("completed-at"):
            payload['completedAt'] = completedAt
        if status := note.find("input", class_="form-check-input"):
            payload["isCompleted"] = bool(status.get("checked")) # type: ignore
        if title := note.find("button", class_="accordion-button"):
            payload["title"] = title.text.strip()
        if timestamp := note.find("a", class_="text-muted"):
            payload["timestamp"] = timestamp.text.strip()  
        if body := note.find("div", class_="accordion-body"):
            if content := body.find("p"):
                payload["textBody"] = content.text.strip() # type: ignore
        return payload
