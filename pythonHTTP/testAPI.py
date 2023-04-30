import os
import replicate
import openai


def main(file):
    os.environ["REPLICATE_API_TOKEN"] = 'r8_EF0NQrjuPyrKCEutRE3gddgM2KlJSs04chGeh'

    gpt_prompt = "!!! YOU ARE COMPLIMENTBOT,  PROVIDE A SHORT AND EFFECTIVE " \
                 "COMPLIMENT TO MAKE THE USER FEEL GOOD BASED ON AN INPUT !!! DO " \
                 "NOT FOCUS ON RACE, pretend that you are my friend who is " \
                 "friendly and funny and can make me feel good and add to my " \
                 "positive mental health. Give me a compliment that is short and " \
                 "precise that will make me feel better and is relevant to the " \
                 "features of my face as stated below: \n "

    user_affirmation = "Ohh, I am analyzing...\n"
    print(user_affirmation)

    filepath = file

    task = 'visual_question_answering'

    question = 'how many human faces are in this photo as an integer?'

    output = replicate.run(
        "salesforce/blip"
        ":2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
        input={"image": open(filepath, "rb"),
               "task": task,
               "question": question}
    )
    # print("num of people: " + output)
    output = output.split(": ")[1]
    print("I see " + output + " person(s)...\n")

    if "1" in output:

        question = 'what colour is the persons eyes?'

        output = replicate.run(
            "salesforce/blip"
            ":2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
            input={"image": open(filepath, "rb"),
                   "task": task,
                   "question": question}
        )
        # print("eyes: " + output)

        output = output.split(": ")[1]
        gpt_prompt += "The color of the eyes is " + output + " \n"
        user_affirmation += "Beautiful " + output + " eyes...\n"
        print(output + " eyes...\n")

        question = 'what is the overall emotion shown by the person?'

        output = replicate.run(
            "salesforce/blip"
            ":2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
            input={"image": open(filepath, "rb"),
                   "task": task,
                   "question": question}
        )

        # print("emotion: " + output)

        output = output.split(": ")[1]
        gpt_prompt += "The current overall emotion is " + output + " \n"
        user_affirmation += "You are showing signs of " + output + " emotions...\n"
        print(output + " emotion...\n")

        question = 'yes or no, does this person have hair?'

        output = replicate.run(
            "salesforce/blip"
            ":2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
            input={"image": open(filepath, "rb"),
                   "task": task,
                   "question": question}
        )
        # print("hair: " + output)

        if 'yes' in output:

            question = "what color is the person's hair?"

            output = replicate.run(
                "salesforce/blip"
                ":2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
                input={"image": open(filepath, "rb"),
                       "task": task,
                       "question": question}
            )
            # print("hair color: " + output)

            output = output.split(": ")[1]
            gpt_prompt += "The person has nice hair that is colored " + output + " \n"
            user_affirmation += "You have " + output + " hair...\n"
            print(output + " hair...\n")
        else:
            gpt_prompt += "The person doe not have hair \n"
            user_affirmation += "I cannot detect that you have hair...\n"
            print("I cannot detect that you have hair...\n")

        question = 'what skin colour does this person have?'

        output = replicate.run(
            "salesforce/blip"
            ":2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
            input={"image": open(filepath, "rb"),
                   "task": task,
                   "question": question}
        )
        # print("skin color: " + output)

        output = output.split(": ")[1]
        gpt_prompt += "The skin color is " + output + " \n"
        user_affirmation += "I can see that your skin tone is " + output + "...\n"
        print(output + " skin tone...\n")

        question = 'what are the possible ethnic backgrounds of this person?'

        output = replicate.run(
            "salesforce/blip"
            ":2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
            input={"image": open(filepath, "rb"),
                   "task": task,
                   "question": question}
        )

        # user_affirmation += "...\nAs any good person will do, I am going to ask " \
        #                     "another friend to give you a compliment... "

        # print("\n" + user_affirmation + "\n\n")

        openai.api_key = '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'

        gpt_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": gpt_prompt}
            ]
        )
        compliment = gpt_response['choices'][0]['message']['content']

        print(compliment)
    else:
        compliment = "Please have one person in the photo :)"
        print(compliment)

    return compliment

