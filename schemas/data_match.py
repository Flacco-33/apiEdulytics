def videoAnalysisEntity(item) -> dict:
    return {
        "_id": item["_id"],
        "idStudent": item["data"]["idStudent"],
        "idTeacher": item["data"]["idTeacher"],
        "idCourse": item["data"]["idCourse"],
        "aspect": item["data"]["aspect"],
        "analysed": item.get("analysed", False),
        "emotions": item["result"]["emotions"]
    }

def textAnalysisEntity(item) -> dict:
    return {
        "_id": item["_id"],
        "idStudent": item["data"]["idStudent"],
        "idTeacher": item["data"]["idTeacher"],
        "idCourse": item["data"]["idCourse"],
        "aspect": item["data"]["aspect"],
        "analysed": item.get("analysed", False),
        "comment": item["data"]["comment"],
        "emotions": item["result"]["emotions"],
        "sentiment": item["result"].get("sentiment")
    }

def matchEntity(video, text) -> dict:
    return {
        "idStudent": video["idStudent"],
        "idTeacher": video["idTeacher"],
        "aspect": video["aspect"],
        "idCourse": video["idCourse"],
        "video_analysis": {
            "emotions": video["emotions"],
        },
        "text_analysis": {
            "comment": text["comment"],
            "emotions": text["emotions"],
            "sentiment": text.get("sentiment")
        }
    }
