import request from '@/utils/request'

export const getSpecimenPhotos = (specimenId) => {
  return request({
    url: `/photos/specimen/${specimenId}`,
    method: 'get'
  })
}

export const getPhotoById = (photoId) => {
  return request({
    url: `/photos/${photoId}`,
    method: 'get'
  })
}

export const uploadPhoto = (specimenId, file, isPrimary = false, caption = null) => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('is_primary', isPrimary)
  if (caption) {
    formData.append('caption', caption)
  }
  return request({
    url: `/photos/specimen/${specimenId}`,
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export const bulkUploadPhotos = (specimenId, files) => {
  const formData = new FormData()
  files.forEach((file) => {
    formData.append('files', file)
  })
  return request({
    url: `/photos/specimen/${specimenId}/bulk`,
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export const setPrimaryPhoto = (photoId) => {
  return request({
    url: `/photos/${photoId}/primary`,
    method: 'put'
  })
}

export const updatePhotoCaption = (photoId, caption) => {
  const formData = new FormData()
  formData.append('caption', caption)
  return request({
    url: `/photos/${photoId}/caption`,
    method: 'put',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export const deletePhoto = (photoId) => {
  return request({
    url: `/photos/${photoId}`,
    method: 'delete'
  })
}
