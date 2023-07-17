from functions import get_authenticated_service, retrieve_phone_numbers, get_reverse_info

# Authenticate and retrieve phone numbers
service = get_authenticated_service()
contacts = retrieve_phone_numbers(service)

# Fetch and print the reverse information for each phone number
for name, phone_number in contacts:
    reverse_info = get_reverse_info(phone_number)
    if reverse_info:
        print(f'{name}: {phone_number} - {reverse_info}')
    else:
        print(f'{name}: {phone_number} - No information available')
