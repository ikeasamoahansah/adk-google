from google.genai import types


def get_and_parse_document(input: types.Part) -> types.Blob:
    """Parses a financial document sent by the user.

    Args:
        input (file): The financial document sent by the user
    
    Returns:
        blob: A structured data in the csv file format with comma separated values
            Includes the total column with for the amount of values in the '$' currency
    """
    pdf_mime_type = "application/pdf"

    pdf_artifact = types.Part(
        inline_data=types.Blob(
            mime_type=pdf_mime_type,
            data=input
        )
    )

    pdf_artifact_alt = types.Part.from_data(data=input, mime_type=pdf_mime_type)
