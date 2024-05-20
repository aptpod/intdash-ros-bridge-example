# intdash ROS Bridge Example

This is an example docker container environemnt for intdash ROS Bridge.

## Demonstration

### Contents of the demo

This demonstration provice following upstream and downstream with intdash.

- Upstream
  - String topic (name: /hello)
  - Poingcloud2 topic (name: /cube_points)
  - Image topic (name: /compressed_image)
- Downstream
  - Joy topic (name: /joy)

ROS2 and ROS are supported.

A data settings file for Data Visualizer (`assets/intdash-ROS-Example.dat`) is provided for your verification.

### Preparation


#### Precondition

Docker and Docker compose are required.

#### Modify .env

Open and edit .env file.

Set each variables to meet your condition.

### Build Docker image

Run following command.

```
docker compose -f docker-compose-(ros2|ros1).yml build
```

### Execute ROS2 demo

Run following command.

```
docker compose -f docker-compose-ros2.yml up
```

### Execute ROS demo

Run following command.

```
docker compose -f docker-compose-ros1.yml up
```

## Customize Docker environment for intdash ROS Bridge

### Add custom message types to intdash ROS Bridge

If you want to add custom message which are not included in ROS base Docker image, you need to rebuild Docker images with your custom message definition.

Copy the source code of your message package to `msg_src/`, then run follwoing command.

```
export PLATFORM=linux/amd64
export ROS_DISTRO=(humble|hoxy|noetic|melodic)
export IMAGE_ARCH=(amd64|arm64v8)
export VERSION=<version of intdash ROS Bridge>
export MIX_ROS1_PACKAGES=<packages of your ROS custom message>
export MIX_ROS2_PACKAGES=<packages of your ROS2 custom message>
export MIX_ACTION_PACKAGES=<packages of your ROS2 custom action>
export TEMPLATE_DOCKERFILE=./custom/tmeplate.(ros2|ros1).Dockerfile
IMAGE_NAME=<your new Docker image name>

docker build --platform $(PLATFORM) \
	--build-arg ROS_DISTRO=$(ROS_DISTRO) \
	--build-arg BASE_IMAGE=public.ecr.aws/aptpod/intdash-ros-bridge \
	--build-arg IMAGE_ARCH=$(IMAGE_ARCH) \
	--build-arg VERSION=$(VERSION) \
	--build-arg MIX_ROS1_PACKAGES="$(MIX_ROS1_PACKAGES)" \
	--build-arg MIX_ROS2_PACKAGES="$(MIX_ROS2_PACKAGES)" \
	--build-arg MIX_ACTION_PACKAGES="$(MIX_ACTION_PACKAGES)" \
	-f $(TEMPLATE_DOCKERFILE) \
	-t $(IMAGE_NAME):$(ROS_DISTRO)-$(VERSION)-$(IMAGE_ARCH) .
```

### Update the agent.yml for intdash Edge Agent2

If you want to change `service/agent/agent2_config.yml`, edit `makge_agent2_config.sh`, then run following command. `service/agent/agent2_config.yml` will be updated.

```
./make_agent2_config.sh 
```

Please refer Aptpod documents how to configure intdash Edge Agent2.
