import pandas as pd
import json
import re


def load_csv_to_json(file_path):
    # Load the CSV file
    df = pd.read_csv(file_path, encoding="utf-8-sig")

    # Convert the DataFrame to a list of dictionaries
    data = df.to_dict("records")

    # Convert each dictionary to a JSON object
    json_data = [json.dumps(record, ensure_ascii=False) for record in data]

    return json_data


def parse_answer(json_obj):
    # Load the JSON object
    data = json.loads(json_obj)

    try:
        # Get the answer field
        answer = data["Response"]

        # Split the answer into sections
        sections = re.split(r"#\s*(\w+)", answer)

        # Initialize a dictionary to hold the parsed answer
        parsed_answer = {}

        # Iterate over the sections
        for i in range(1, len(sections), 2):
            # Get the section title
            title = sections[i]

            # Get the section content
            content = sections[i + 1].strip()

            content = content.strip()
            if content.startswith("：") or content.startswith(":"):
                content = content[1:]
            content = content.strip()

            parsed_answer[title] = content

        knowledge_points = re.findall(
            r"【(.*?)】(.*?)(?=【|$)", parsed_answer["知识点"], re.DOTALL
        )
        if len(knowledge_points) == 0:
            raise Exception("No knowledge points found")
        parsed_answer["知识点"] = [
            {"title": kp[0], "content": re.sub(r"^\s*[：\:]", "", kp[1]).strip()}
            for kp in knowledge_points
        ]

        # Replace the answer field with the parsed answer
        data["Answer"] = parsed_answer

    except Exception as e:
        print(f"Error parsing JSON object: {e}")
        return None

    return data


if __name__ == "__main__":
    # Load the CSV file and convert it to JSON
    json_data = load_csv_to_json("data/课后测验.csv")

    # Parse the answer field of each JSON object
    parsed_data = []
    for i, json_obj in enumerate(json_data):
        parsed_obj = parse_answer(json_obj)
        if parsed_obj is None:
            print(f"Error occurred at row {i+1}")
        else:
            parsed_data.append(parsed_obj)

    # Create a list of 知识点
    knowledge_points = []
    for data in parsed_data:
        for kp in data["Answer"]["知识点"]:
            knowledge_points.append(kp)

    # Convert the list of 知识点 to a DataFrame
    df = pd.DataFrame(knowledge_points)

    # Group the DataFrame by the 'title' column and merge the 'content' of each group
    df = df.groupby("title")["content"].apply("\n￥￥\n".join).reset_index()

    # Sort the DataFrame by the 'title' column
    df = df.sort_values("title")

    # Save the DataFrame as a CSV file
    df.to_csv("knowledge_points.csv", index=False, encoding="utf-8-sig")
