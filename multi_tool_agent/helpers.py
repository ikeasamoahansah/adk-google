from google.genai import types
from google.adk.agents.callback_context import CallbackContext

# def get_and_load_dcument()

async def save_document(context: CallbackContext, report_bytes: bytes):
    """Saves generated PDF report bytes as an artifact."""
    report_artifact = types.Part.from_data(
        data=report_bytes,
        mime_type="application/pdf"
    )
    filename = "generated_report.pdf"

    try:
        version = context.save_artifact(filename=filename, artifact=report_artifact)
        print(f"Successfully saved artifact '{filename}' as version {version}.")
        # The event generated after this callback will contain:
        # event.actions.artifact_delta == {"generated_report.pdf": version}
    except ValueError as e:
        print(f"Error saving artifact: {e}. Is ArtifactService configured?")
    except Exception as e:
        # Handle potential storage errors (e.g., GCS permissions)
        print(f"An unexpected error occurred during artifact save: {e}")


async def process_latest_report(context: CallbackContext):
    """Loads the latest report artifact and processes its data."""
    filename = "generated_report.pdf"
    try:
        # Load the latest version
        report_artifact = context.load_artifact(filename=filename)

        if report_artifact and report_artifact.inline_data:
            print(f"Successfully loaded latest artifact '{filename}'.")
            print(f"MIME Type: {report_artifact.inline_data.mime_type}")
            # Process the report_artifact.inline_data.data (bytes)
            pdf_bytes = report_artifact.inline_data.data
            print(f"Report size: {len(pdf_bytes)} bytes.")
            # ... further processing ...
        else:
            print(f"Artifact '{filename}' not found.")

        # Example: Load a specific version (if version 0 exists)
        # specific_version_artifact = context.load_artifact(filename=filename, version=0)
        # if specific_version_artifact:
        #     print(f"Loaded version 0 of '{filename}'.")

    except ValueError as e:
        print(f"Error loading artifact: {e}. Is ArtifactService configured?")
    except Exception as e:
        # Handle potential storage errors
        print(f"An unexpected error occurred during artifact load: {e}")


