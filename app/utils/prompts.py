
def main_prompt(input, retrievedDocs):
    main_prompt = f"""
                Answer properly

                user_input:{input}
                context(if empty, ignore it):{retrievedDocs}
                """
    
    return main_prompt