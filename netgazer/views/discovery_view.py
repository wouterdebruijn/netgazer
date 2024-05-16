import asyncio
from asyncio.subprocess import Process
import json
import uuid
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.views import View


running_task: Process | None = None
is_reading: bool = False


class AsyncView(View):
    # Stream the output of the process
    async def stream_output(self):
        global running_task
        global is_reading

        # Set is_reading to True
        is_reading = True

        while True:
            # Read line from stdout
            line = await running_task.stdout.readline()

            # If process has finished, break the loop
            if line == b'' or running_task.returncode is not None:
                is_reading = False
                break

            # Yield line to the client
            yield line.decode("utf-8")

    async def get(self, request, *args, **kwargs):
        global running_task
        global is_reading

        if running_task is None or running_task.returncode is not None:
            return HttpResponse("No discovery process is running\n", status=200)

        if is_reading:
            return HttpResponse("Connection already established\n", status=200)

        return StreamingHttpResponse(self.stream_output())

    async def post(self, request, *args, **kwargs):
        global running_task

        # Get the IPv4 address from the request
        ipv4 = request.POST.get('ipv4')

        if ipv4 is None:
            return JsonResponse({"error": "IPv4 address is required!"}, status=400)

        # Generate a unique ID for this discovery process
        async_id = uuid.uuid4()

        # Start discovery process without waiting for it to finish
        running_task = await asyncio.create_subprocess_exec(
            'python', 'netgazer_cli.py', 'discover', ipv4, str(async_id),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )

        return JsonResponse({"async_id": str(async_id)}, status=200)
