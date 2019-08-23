defmodule Cams.Snapshots do
  use Task

  def child_spec(opts) do
    %{
      id: __MODULE__,
      start: {__MODULE__, :start_link, [opts]},
      type: :worker,
      restart: :permanent
    }
  end

  def start_link(opts) do
    Task.start_link(__MODULE__, :takeSnapshot, opts)
  end

  def initCam(cam) do
    IO.puts("Initializing esp32-cam settings")
    base_url = cam
    flip_vertical = to_charlist("http://#{base_url}/control?var=vflip&val=1")
    flip_horizontal = to_charlist("http://#{base_url}/control?var=hmirror&val=1")
    resolution = to_charlist("http://#{base_url}/control?var=framesize&val=10")
    {:ok, _} = :httpc.request(flip_vertical)
    {:ok, _} = :httpc.request(flip_horizontal)
    {:ok, _} = :httpc.request(resolution)
  end

  def processSnapshot({:ok, {{_http_version, 200, 'OK'}, _headers, body}}, cam) do
    min_expected_size = 80_000
    body_size = length(body)

    if body_size < min_expected_size do
      IO.puts("bytes: #{body_size}")
      initCam(cam)
    else
      outout_dir = "images/#{cam}"
      timestamp = :os.system_time(:seconds)
      filename = "#{outout_dir}/#{timestamp}.jpg"
      IO.puts("#{filename}")

      {:ok, file} = File.open(filename, [:write])
      IO.binwrite(file, body)
      File.close(file)
    end
  end

  def processSnapshot({:error, reason}, cam) do
    wait_time = 5000
    IO.inspect(reason)
    IO.puts("Waiting #{wait_time / 1000} seconds for #{cam}.")
    :timer.sleep(wait_time)
  end

  def takeSnapshot(cam, snapshot_interval) do
    url = to_charlist("http://#{cam}/capture")
    timeout = 5000
    processSnapshot(:httpc.request(:get, {url, []}, [{:timeout, timeout}], []), cam)
    :timer.sleep(snapshot_interval * 1000)
    takeSnapshot(cam, snapshot_interval)
  end
end

Application.ensure_all_started(:inets)
# Application.ensure_all_started(:ssl)

Supervisor.start_link(
  [
    {Cams.Snapshots, ["CAM_URL", 1]}
  ],
  strategy: :one_for_one,
  max_seconds: 1,
  max_restarts: 10
)

receive do
  {:killmewtf} ->
    IO.puts("bye")
end
